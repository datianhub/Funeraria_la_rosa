from django.urls import path
from . import views
from django.views.generic import TemplateView


urlpatterns = [
    #Login and Logout
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    #Others
    path('', views.titular_dashboard, name='dashboard'),
    path('config/', views.config_dashboard ,name="config"),
    path('config/editar/<int:pk>/', views.editar_configuracion, name='editar_configuracion'),
    path('titulares/', views.titular_list, name='titular_list'),
    path('titulares/registro', views.crear_titular, name='titular_registro'),
    path('titulares/registro/beneficiario', views.crear_beneficiario, name='beneficiario_registro'),
    path('titulares/registro/mascota', views.crear_mascota, name='crear_mascota'),
    # AJAX endpoints
    path('obtener-contrato/<int:titular_id>/', views.obtener_contrato, name='obtener_contrato'),
    path('obtener-miembros/<int:titular_id>/', views.obtener_miembros_paginados, name='obtener_miembros_paginados'),
]