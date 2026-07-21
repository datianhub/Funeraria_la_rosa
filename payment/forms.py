from django import forms
from .models import Plan

class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ['valor_mensual', 'valor_mascotas', 'valor_beneficiario_extra', 'valor_cobro_edad', 'edad_maxima']
        widgets = {
            'valor_mensual': forms.NumberInput(attrs={'class': 'form-input'}),
            'valor_mascotas': forms.NumberInput(attrs={'class': 'form-input'}),
            'valor_beneficiario_extra': forms.NumberInput(attrs={'class': 'form-input'}),
            'valor_cobro_edad': forms.NumberInput(attrs={'class': 'form-input'}),
            'edad_maxima': forms.NumberInput(attrs={'class': 'form-input'})
        }