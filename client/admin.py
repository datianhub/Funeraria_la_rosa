from django.contrib import admin

# Register your models here.
from .models import Titular, Beneficiario, Mascota

admin.site.register(Titular)
admin.site.register(Beneficiario)
admin.site.register(Mascota)

