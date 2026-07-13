from django.contrib import admin
from .models import Factura, Pago

# Register your models here.
admin.site.register(Pago)
admin.site.register(Factura)
