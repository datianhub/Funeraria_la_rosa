from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import Count, Q, Sum
from django.views.decorators.http import require_POST

from .models import Factura, Pago, Plan
from .services import generar_factura_para_pago
from client.models import Mascota, Beneficiario


# Create your views here.
def payments_dashboard(request):
    query = request.GET.get('q', '').strip()
    query_date_inicio = request.GET.get('fecha_inicio', '').strip()
    query_date_fin = request.GET.get('fecha_fin', '').strip()

    pagos = Pago.objects.select_related('titular').annotate(
        beneficiarios_count=Count('titular__beneficiarios', distinct=True),
        mascotas_count=Count('titular__mascotas', distinct=True),
    ).order_by('-id')

    if query:
        pagos = pagos.filter(
            Q(titular__cedula__icontains=query) |
            Q(titular__nombre__icontains=query) |
            Q(titular__apellido__icontains=query) |
            Q(titular__numero_contrato__icontains=query)
        )

    if query_date_inicio and query_date_fin:
        pagos = pagos.filter(fecha_ultimo_pago__date__range=[query_date_inicio, query_date_fin])

    resumen = pagos.aggregate(total_recaudo=Sum('monto_total_a_pagar'))

    pagos_vencidos = sum(
        1 for pago in pagos if pago.esta_vencido
    )

    pagos_activos = sum(
        1 for pago in pagos if not pago.esta_vencido
    )

    context = {
        'pagos': pagos,
        'query': query,
        'fecha_inicio': query_date_inicio,
        'fecha_fin': query_date_fin,
        'total_recaudo': resumen['total_recaudo'] or 0,
        'pagos_vencidos': pagos_vencidos,
        'pagos_activos': pagos_activos,
    }
    return render(request, 'payments/pay.html', context)


@require_POST
def generar_factura(request, pago_id):
    factura, _ = generar_factura_para_pago(pago_id)
    return redirect('invoice_detail', factura_id=factura.id)


def invoice_detail(request, factura_id):
    factura = get_object_or_404(
        Factura.objects.select_related('titular', 'pago'),
        pk=factura_id,
    )

    context = {
        'factura': factura,
        'beneficiarios_count': factura.titular.beneficiarios.count(),
        'mascotas_count': factura.titular.mascotas.count(),
    }
    return render(request, 'payments/invoice.html', context)

def calcular_monto_plan(id_titular):
    try:
        plan = Plan.objects.first()
        
        with transaction.atomic():
            pago_titular_asociado = Pago.objects.get(titular_id=id_titular)
            tarifa_mensual = plan.valor_mensual

            mascotas_asociadas = Mascota.objects.filter(titular_id=id_titular).count()
            if mascotas_asociadas > 0:
                tarifa_mensual += (mascotas_asociadas * plan.valor_mascotas)

            beneficiarios_asociados = Beneficiario.objects.filter(titular_id=id_titular)
            beneficiarios_asociados_cantidad = beneficiarios_asociados.count()
            if beneficiarios_asociados_cantidad > 5:
                beneficiarios_extra = beneficiarios_asociados_cantidad - 5
                tarifa_mensual += (beneficiarios_extra * plan.valor_beneficiario_extra)

            mayores_de_rango_edad = beneficiarios_asociados.filter(edad_afiliacion__gt=65, cobro_edad_aplicado=False)
            nuevos_recargos_unicos = 0
            for b in mayores_de_rango_edad:
                monto_extra_por_edad = b.edad_afiliacion - 65
                nuevos_recargos_unicos += (monto_extra_por_edad * plan.valor_cobro_edad)

                b.cobro_edad_aplicado = True
                b.save()

            pago_titular_asociado.monto_mensual_tarifa = tarifa_mensual
            pago_titular_asociado.monto_cargos_unicos += nuevos_recargos_unicos
            pago_titular_asociado.guardar_totales()

    except Pago.DoesNotExist:
        raise ObjectDoesNotExist(f"No se encontró un registro de Pago para el titular con ID {id_titular}")


    
