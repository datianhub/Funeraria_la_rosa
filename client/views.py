from django.shortcuts import render
from django.template import loader
from django.db.models import Q
from .models import Titular, Beneficiario, Mascota
from django.http import HttpResponse, JsonResponse
from .forms import TitularForm, BeneficiarioForm, MascotaForm
from django.shortcuts import redirect
from django.core.paginator import Paginator
from payment.models import Pago
from payment.views import calcular_monto_plan
from django.core.paginator import Paginator
from dateutil.relativedelta import relativedelta


def titular_list(request):

    print("peticion desde:", request)

    query = request.GET.get('q', '').strip()

    query_date_inicio = request.GET.get('fecha_inicio', '').strip()
    query_date_fin = request.GET.get('fecha_fin', '').strip()

    titulares = Titular.objects.order_by('-id')

    form = TitularForm()
    form_beneficiario = BeneficiarioForm()
    form_mascota = MascotaForm()

    if query:
        titulares = titulares.filter(
            Q(cedula__icontains=query) |
            Q(nombre__icontains=query) |
            Q(apellido__icontains=query) |
            Q(numero_contrato__icontains=query) |
            Q(beneficiarios__nombre_completo__icontains=query) |
            Q(beneficiarios__cedula__icontains=query),
        ).distinct()

    if query_date_inicio and query_date_fin:
        titulares = titulares.filter(
            fecha_ingreso__range=[query_date_inicio, query_date_fin]
        )

    context = {
        'query': query,
        'titulares': titulares,
        'form' : form,
        'form_beneficiario' : form_beneficiario,
        'form_mascota' : form_mascota,
        'fecha_inicio': query_date_inicio,
        'fecha_fin': query_date_fin
    }
    return render(request, 'titular.html', context)


def titular_dashboard(request):
    titulares_count = Titular.objects.count()
    return render(request, 'dashboard.html', {'titulares_count': titulares_count})


def crear_titular(request):
    form = TitularForm(request.POST or None)
    titulares = Titular.objects.order_by('-id')
    if request.method == 'POST' and form.is_valid():
        nuevo_titular = form.save()
        crear_primer_pago(nuevo_titular)
        return redirect('titular_list')
    context = {
        'form' : form,
        'titulares': titulares
    }
    return render(request, 'titular.html', context)


def crear_primer_pago(titular_instacia):
    pago = Pago(titular=titular_instacia, monto_mensual_tarifa=24000.00, monto_total_a_pagar=24000.00, monto_cargos_unicos=0)
    pago.proximo_pago = (
        pago.titular.fecha_ingreso + relativedelta(months=1)
    )
    pago.save()
    return True

def crear_beneficiario(request):
    if request.method == 'POST':
        form_beneficiario = BeneficiarioForm(request.POST)
        
        if form_beneficiario.is_valid():
            beneficiario = form_beneficiario.save()
            calcular_monto_plan(beneficiario.titular.id)

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            return redirect('titular_list')
        
        context = {'form_beneficiario': form_beneficiario}
        return render(request, 'registro_beneficiario.html', context)
    
    form_beneficiario = BeneficiarioForm()
    return render(request, 'registro_beneficiario.html', {'form_beneficiario': form_beneficiario})

def crear_mascota(request):
    if request.method == 'POST':
        form_mascota = MascotaForm(request.POST)
        print(request.POST)
        if form_mascota.is_valid():
            mascota = form_mascota.save()
            calcular_monto_plan(mascota.titular.id)
            
            # Si es una petición AJAX/Fetch, respondemos con JSON
            if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
                return JsonResponse({
                    'success': True,
                    'mascota': {
                        'id': mascota.id,
                        'nombre': mascota.nombre,
                        'especie': mascota.especie,
                        # Puedes agregar aquí la fecha de afiliación si tu modelo la tiene:
                        # 'fecha': mascota.fecha_afiliacion.strftime('%d/%m/%Y') 
                    }
                })
            
            return redirect('titular_list') # Respaldo si no es AJAX
        
        # Si el formulario es inválido y es AJAX, devolvemos los errores
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'errors': form_mascota.errors}, status=400)
            
    form_mascota = MascotaForm()
    return render(request, 'crearMascotaFormModal.html', {'form_mascota': form_mascota})


# Paginación
def obtener_miembros_paginados(request, titular_id):
    beneficiarios = list(Beneficiario.objects.filter(titular_id=titular_id).values('id', 'nombre_completo', 'cedula', 'parentesco', 'edad_afiliacion', 'fecha_afiliacion'))
    mascotas = list(Mascota.objects.filter(titular_id=titular_id).values('id', 'nombre', 'especie', 'fecha_afiliacion'))

    lista_mascotas = [
        {
            'id': m['id'],
            'nombre_completo': f"{m['nombre']} (🐾 Mascota)",
            'cedula': '-',
            'parentesco': m['especie'],
            'edad_afiliacion': '-',
            'fecha_afiliacion': m['fecha_afiliacion'],
        } for m in mascotas
    ]
    
    todos_los_miembros = beneficiarios + lista_mascotas

    elementos_por_pagina = 6
    paginator = Paginator(todos_los_miembros, elementos_por_pagina)
    
    numero_pagina = request.GET.get('page', 1)
    pagina_actual = paginator.get_page(numero_pagina)

    return JsonResponse({
        'resultados': pagina_actual.object_list,
        'tiene_siguiente': pagina_actual.has_next(),
        'tiene_anterior': pagina_actual.has_previous(),
        'pagina_actual': pagina_actual.number,
        'total_paginas': paginator.num_pages
    })

"""
Vista de Configuración
"""
def config_dashboard(request):
    return render(request, "settings/conf.html")
    