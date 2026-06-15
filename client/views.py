from django.shortcuts import render
from django.template import loader
from django.db.models import Q
from .models import Titular, Beneficiario
from django.http import HttpResponse, JsonResponse
from .forms import TitularForm, BeneficiarioForm
from django.shortcuts import redirect
from django.core.paginator import Paginator

def titular_list(request):

    print("peticion desde:", request)

    query = request.GET.get('q', '').strip()

    query_date_inicio = request.GET.get('fecha_inicio', '').strip()
    query_date_fin = request.GET.get('fecha_fin', '').strip()

    titulares = Titular.objects.order_by('-id')

    form = TitularForm()
    form_beneficiario = BeneficiarioForm()

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
        'fecha_inicio': query_date_inicio,
        'fecha_fin': query_date_fin
    }
    return render(request, 'titular.html', context)


def titular_dashboard(request):
    titulares_count = Titular.objects.count()
    return render(request, 'dashboard.html', {'titulares_count': titulares_count})


def crear_titular(request):
    form = TitularForm(request.POST or None)
    print(form)
    titulares = Titular.objects.order_by('-id')
    if request.method == 'POST' and form.is_valid():
        form.save() 
        return redirect('titular_list')
    context = {
        'form' : form,
        'titulares': titulares
    }
    return render(request, 'titular.html', context)


def crear_beneficiario(request):
    if request.method == 'POST':
        form_beneficiario = BeneficiarioForm(request.POST)
        
        if form_beneficiario.is_valid():
            form_beneficiario.save()

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            return redirect('titular_list')
        
        context = {'form_beneficiario': form_beneficiario}
        return render(request, 'registro_beneficiario.html', context)
    
    form_beneficiario = BeneficiarioForm()
    return render(request, 'registro_beneficiario.html', {'form_beneficiario': form_beneficiario})

def beneficiario_list(request, titular_id):
    beneficiarios = Beneficiario.objects.filter(titular_id=titular_id).order_by('-id')
    return render(request, 'beneficiario.html', {'beneficiarios': beneficiarios})

def beneficiarios_por_titular_api(request, titular_id):
    beneficiarios = Beneficiario.objects.filter(titular_id=titular_id).values(
        'nombre_completo', 'cedula', 'parentesco', 'edad_actual', 'fecha_afiliacion'
    )
    return JsonResponse({'beneficiarios': list(beneficiarios)})