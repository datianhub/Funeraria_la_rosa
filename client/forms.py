from django import forms
from .models import Titular, Beneficiario

class TitularForm(forms.ModelForm):
    class Meta:
        model = Titular
        fields = '__all__'

        widgets = {
            'cedula': forms.TextInput(attrs={
                'class': 'w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-[#5a2a3b] focus:border-[#5a2a3b] p-2.5 transition-colors',
                'placeholder': 'Ej: 10203040'
            }),
            'numero_contrato': forms.NumberInput(attrs={
                'class': 'w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-[#5a2a3b] focus:border-[#5a2a3b] p-2.5 transition-colors',
                'placeholder': 'Nombre de contrato'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-[#5a2a3b] focus:border-[#5a2a3b] p-2.5 transition-colors',
                'placeholder': 'Ej: 10203040'
            }),
            'apellido': forms.TextInput(attrs={
                'class': 'w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-[#5a2a3b] focus:border-[#5a2a3b] p-2.5 transition-colors',
                'placeholder': 'Apellido del titular'
            }),
            'sexo': forms.Select(attrs={
                'class' : 'w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-[#5a2a3b] focus:border-[#5a2a3b] p-2.5 transition-colors'
            }),
            'edad': forms.NumberInput(attrs={
                'class' : 'w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-[#5a2a3b] focus:border-[#5a2a3b] p-2.5 transition-colors'
            }),
            'estado_civil': forms.TextInput(attrs={
                'class': 'w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-[#5a2a3b] focus:border-[#5a2a3b] p-2.5 transition-colors',
                'placeholder': 'Ej: 10203040'
            }),
            'ocupacion': forms.TextInput(attrs={
            'class': 'w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-[#5a2a3b] focus:border-[#5a2a3b] p-2.5 transition-colors',
            'placeholder': 'Apellido del titular'
            }),
            'direccion': forms.TextInput(attrs={
            'class' : 'w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-[#5a2a3b] focus:border-[#5a2a3b] p-2.5 transition-colors'
            }),
            'telefono': forms.NumberInput(attrs={
                'class' : 'w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-[#5a2a3b] focus:border-[#5a2a3b] p-2.5 transition-colors'
            }),
            'fecha_ingreso': forms.DateInput(attrs={
            'class' : 'w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-[#5a2a3b] focus:border-[#5a2a3b] p-2.5 transition-colors'
            })
        }

class BeneficiarioForm(forms.ModelForm):
    class Meta:
        model = Beneficiario
        fields = '__all__'
        
        widgets = {
            'titular': forms.HiddenInput(),
            
            'nombre_completo': forms.TextInput(attrs={
                'class': 'w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-[#5a2a3b] focus:border-[#5a2a3b] p-2.5 transition-colors',
                'placeholder': 'Nombre completo del beneficiario'
            }),
            'cedula': forms.TextInput(attrs={  
                'class': 'w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-[#5a2a3b] focus:border-[#5a2a3b] p-2.5 transition-colors',
                'placeholder': 'Ej: 10203040'
            }),
            'parentesco': forms.TextInput(attrs={
                'class': 'w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-[#5a2a3b] focus:border-[#5a2a3b] p-2.5 transition-colors',
                'placeholder': 'Ej: Hijo, Cónyuge, Madre...'
            }),
            'edad_afiliacion': forms.NumberInput(attrs={
                'class': 'w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-[#5a2a3b] focus:border-[#5a2a3b] p-2.5 transition-colors',
                'placeholder': 'Edad al afiliarse'
            }),
            'edad_actual': forms.NumberInput(attrs={
                'class': 'w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-[#5a2a3b] focus:border-[#5a2a3b] p-2.5 transition-colors',
                'placeholder': 'Edad actual'
            }),
            'fecha_afiliacion': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-[#5a2a3b] focus:border-[#5a2a3b] p-2.5 transition-colors'
            }),
            
            'mascota': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-[#5a2a3b] bg-gray-100 border-gray-300 rounded focus:ring-[#5a2a3b]',
                'onchange' : 'ableFilePetType()'
            }),
            'tipo_mascota': forms.TextInput(attrs={
                'class': 'disabled:opacity-75 w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-[#5a2a3b] focus:border-[#5a2a3b] p-2.5 transition-colors ',
                'placeholder': 'Ej: Perro, Gato...',
                'disabled' : True
            }),
            'notas': forms.Textarea(attrs={
                'class': 'w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-[#5a2a3b] focus:border-[#5a2a3b] p-2.5 transition-colors',
                'rows': 3,
                'placeholder': 'Observaciones adicionales...'
            }),
        }