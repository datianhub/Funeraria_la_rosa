from django.urls import path
from . import views
from django.views.generic import TemplateView


urlpatterns = [
    path('', views.titular_dashboard, name='dashboard'),
    path('config/', views.config_dashboard ,name="config"),
    path('titulares/', views.titular_list, name='titular_list'),
    path('titulares/registro', views.crear_titular, name='titular_registro'),
    path('titulares/registro/beneficiario', views.crear_beneficiario, name='beneficiario_registro'),
    path('titulares/registro/mascota', views.crear_mascota, name='crear_mascota'),
    path('obtener-miembros/<int:titular_id>/', views.obtener_miembros_paginados, name='obtener_miembros_paginados'),
]