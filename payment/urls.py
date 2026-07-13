from django.urls import path
from . import views

urlpatterns = [
    path('pagos/', views.payments_dashboard, name='payments'),
    path('pagos/<int:pago_id>/factura/', views.generar_factura, name='generate_invoice'),
    path('facturas/<int:factura_id>/', views.invoice_detail, name='invoice_detail'),
]

