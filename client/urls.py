from django.urls import path
from . import views
from django.views.generic import TemplateView



urlpatterns = [
    path('', views.titular_dashboard, name='dashboard'),
    path('titulares/', views.titular_list, name='titular_list'),
    path('titulares/registro', views.crear_titular, name='titular_registro'),
    path('titulares/registro/beneficiario', views.crear_beneficiario, name='beneficiario_registro'),
    path('api/titulares/<int:titular_id>/beneficiarios/', views.beneficiarios_por_titular_api, name='api_beneficiarios'),
]