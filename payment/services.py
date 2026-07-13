from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from .models import Factura, Pago
from dateutil.relativedelta import relativedelta
from django.utils import timezone

def calcular_proximo_pago(pago):
    fecha_base = (
            pago.proximo_pago
            or pago.titular.fecha_ingreso
            or timezone.localdate()
        )

    if not pago.proximo_pago:
        return fecha_base + relativedelta(months=1)

    return fecha_base + relativedelta(months=1)


def generar_factura_para_pago(pago_id):

    with transaction.atomic():

        pago = (
            Pago.objects
            .select_for_update()
            .select_related("titular")
            .get(pk=pago_id)
        )

        fecha_periodo = (
            pago.proximo_pago
            or pago.titular.fecha_ingreso
            or timezone.localdate()
        )

        factura, creada = Factura.objects.get_or_create(
            pago=pago,
            titular=pago.titular,
            periodo_anio=fecha_periodo.year,
            periodo_mes=fecha_periodo.month,
            defaults={
                "monto_mensual_tarifa": pago.monto_mensual_tarifa,
                "monto_cargos_unicos": pago.monto_cargos_unicos,
                "monto_total": pago.monto_total_a_pagar,
            }
        )

        if creada:
            pago.fecha_ultimo_pago = timezone.now()
            pago.proximo_pago = calcular_proximo_pago(pago)
            pago.plan_vencido = False
            pago.monto_cargos_unicos = Decimal("0.00")
            pago.guardar_totales()

            if not pago.titular.plan_activo:
                pago.titular.plan_activo = True
                pago.titular.save(update_fields=["plan_activo"])

        return factura, creada
