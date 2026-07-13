from django import forms
from .models import Titular, Beneficiario, Mascota

class TitularForm(forms.ModelForm):
    class Meta:
        model = Titular
        fields = '__all__'

        widgets = {
            'cedula': forms.TextInput(attrs={
                'class': "w-full bg-white border border-[#D4B96A]/40 text-[#2C1F0E] text-xs rounded-lg focus:ring-4 focus:ring-[#D4B96A]/10 focus:border-[#D4B96A] p-2 outline-none transition-all font-['Inter',sans-serif]",
                'placeholder': 'Ej: 10203040'
            }),
            'numero_contrato': forms.NumberInput(attrs={
                'class': "w-full bg-white border border-[#D4B96A]/40 text-[#2C1F0E] text-xs rounded-lg focus:ring-4 focus:ring-[#D4B96A]/10 focus:border-[#D4B96A] p-2 outline-none transition-all font-['Inter',sans-serif]",
                'placeholder': 'N° de contrato'
            }),
            'nombre': forms.TextInput(attrs={
                'class': "w-full bg-white border border-[#D4B96A]/40 text-[#2C1F0E] text-xs rounded-lg focus:ring-4 focus:ring-[#D4B96A]/10 focus:border-[#D4B96A] p-2 outline-none transition-all font-['Inter',sans-serif]",
                'placeholder': 'Nombre del titular'
            }),
            'apellido': forms.TextInput(attrs={
                'class': "w-full bg-white border border-[#D4B96A]/40 text-[#2C1F0E] text-xs rounded-lg focus:ring-4 focus:ring-[#D4B96A]/10 focus:border-[#D4B96A] p-2 outline-none transition-all font-['Inter',sans-serif]",
                'placeholder': 'Apellido del titular'
            }),
            'sexo': forms.Select(attrs={
                'class': "w-full bg-white border border-[#D4B96A]/40 text-[#2C1F0E] text-xs rounded-lg focus:ring-4 focus:ring-[#D4B96A]/10 focus:border-[#D4B96A] p-2 outline-none transition-all font-['Inter',sans-serif] appearance-none bg-[url('data:image/svg+xml,%3Csvg_xmlns=%22http://www.w3.org/2000/svg%22_fill=%22none%22_viewBox=%220_0_24_24%22_stroke=%22%23D4B96A%22%3E%3Cpath_stroke-linecap=%22round%22_stroke-linejoin=%22round%22_stroke-width=%222%22_d=%22M19_9l-7_7-7-7%22%3E%3C/path%3E%3C/svg%3E')] bg-no-repeat bg-[right_10px_center] bg-[length:14px] pr-8 cursor-pointer"
            }),
            'edad': forms.NumberInput(attrs={
                'class': "w-full bg-white border border-[#D4B96A]/40 text-[#2C1F0E] text-xs rounded-lg focus:ring-4 focus:ring-[#D4B96A]/10 focus:border-[#D4B96A] p-2 outline-none transition-all font-['Inter',sans-serif]",
                'placeholder': 'Edad'
            }),
            'estado_civil': forms.TextInput(attrs={
                'class': "w-full bg-white border border-[#D4B96A]/40 text-[#2C1F0E] text-xs rounded-lg focus:ring-4 focus:ring-[#D4B96A]/10 focus:border-[#D4B96A] p-2 outline-none transition-all font-['Inter',sans-serif]",
                'placeholder': 'Ej: Soltero/a, Casado/a'
            }),
            'ocupacion': forms.TextInput(attrs={
                'class': "w-full bg-white border border-[#D4B96A]/40 text-[#2C1F0E] text-xs rounded-lg focus:ring-4 focus:ring-[#D4B96A]/10 focus:border-[#D4B96A] p-2 outline-none transition-all font-['Inter',sans-serif]",
                'placeholder': 'Ej: Empleado, Pensionado'
            }),
            'direccion': forms.TextInput(attrs={
                'class': "w-full bg-white border border-[#D4B96A]/40 text-[#2C1F0E] text-xs rounded-lg focus:ring-4 focus:ring-[#D4B96A]/10 focus:border-[#D4B96A] p-2 outline-none transition-all font-['Inter',sans-serif]",
                'placeholder': 'Dirección de residencia completa'
            }),
            'telefono': forms.NumberInput(attrs={
                'class': "w-full bg-white border border-[#D4B96A]/40 text-[#2C1F0E] text-xs rounded-lg focus:ring-4 focus:ring-[#D4B96A]/10 focus:border-[#D4B96A] p-2 outline-none transition-all font-['Inter',sans-serif]",
                'placeholder': 'Ej: 3001234567'
            }),
            'fecha_ingreso': forms.DateInput(attrs={
                'class': "w-full bg-white border border-[#D4B96A]/40 text-[#2C1F0E] text-xs rounded-lg focus:ring-4 focus:ring-[#D4B96A]/10 focus:border-[#D4B96A] p-2 outline-none transition-all font-['Inter',sans-serif] cursor-pointer",
                'type': 'date'
            })
        }

class BeneficiarioForm(forms.ModelForm):
    class Meta:
        model = Beneficiario
        fields = '__all__'
        
        widgets = {
            'titular': forms.HiddenInput(),
            
            'nombre_completo': forms.TextInput(attrs={
                'class': "w-full bg-white border border-[#D4B96A]/40 text-[#2C1F0E] text-xs rounded-lg focus:ring-4 focus:ring-[#D4B96A]/10 focus:border-[#D4B96A] p-2 outline-none transition-all font-['Inter',sans-serif]",
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
            'fecha_afiliacion': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-[#5a2a3b] focus:border-[#5a2a3b] p-2.5 transition-colors'
            }),
            'notas': forms.Textarea(attrs={
                'class': 'w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-[#5a2a3b] focus:border-[#5a2a3b] p-2.5 transition-colors',
                'rows': 3,
                'placeholder': 'Observaciones adicionales...'
            }),
        }

class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = '__all__'

        widgets = {
            'titular' : forms.HiddenInput(attrs={'id': 'id_titular_mascota'}),
            'nombre': forms.TextInput(attrs={
                'class': "w-full bg-white border border-[#D4B96A]/40 text-[#2C1F0E] text-xs rounded-lg focus:ring-4 focus:ring-[#D4B96A]/10 focus:border-[#D4B96A] p-2 outline-none transition-all font-['Inter',sans-serif]",
                'placeholder': 'Nombre de la mascota'
            }),
            'especie': forms.TextInput(attrs={
                'class': "w-full bg-white border border-[#D4B96A]/40 text-[#2C1F0E] text-xs rounded-lg focus:ring-4 focus:ring-[#D4B96A]/10 focus:border-[#D4B96A] p-2 outline-none transition-all font-['Inter',sans-serif]",
                'placeholder': 'Ej: Perro, gato.'
            }),
            'fecha_afiliacion': forms.DateInput(attrs={
                'type': 'date'
            }),
        }