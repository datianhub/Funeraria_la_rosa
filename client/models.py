from django.db import models
from django.core.exceptions import ValidationError

class Titular(models.Model):

    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]

    cedula = models.BigIntegerField(unique=True)
    numero_contrato = models.IntegerField(unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    edad = models.PositiveSmallIntegerField(null=True, blank=True)
    estado_civil = models.CharField(max_length=50, null=True, blank=True)
    ocupacion = models.CharField(max_length=150, null=True, blank=True)
    direccion = models.CharField(max_length=255)
    telefono = models.BigIntegerField()
    fecha_ingreso = models.DateField()

    class Meta:
        db_table = 'Titular'
        verbose_name = 'Titular'
        verbose_name_plural = 'Titulares'

    def __str__(self):
        return f"{self.nombre} {self.apellido} — CC: {self.cedula}"


class Beneficiario(models.Model):

    titular = models.ForeignKey(
        Titular,
        on_delete=models.CASCADE,
        related_name='beneficiarios'
    )
    nombre_completo = models.CharField(max_length=200)
    cedula = models.BigIntegerField(unique=True)
    parentesco = models.CharField(max_length=100)
    edad_afiliacion = models.PositiveSmallIntegerField()
    edad_actual = models.PositiveSmallIntegerField()
    fecha_afiliacion = models.DateField(auto_now_add=True)
    mascota = models.BooleanField(default=False)
    tipo_mascota = models.CharField(max_length=100, null=True, blank=True)
    notas = models.TextField(null=True, blank=True)

    def clean(self):
        if not self.mascota and self.tipo_mascota:
            raise ValidationError("No se puede definir tipo de mascota si 'mascota' es False.")
        if self.mascota and not self.tipo_mascota:
            raise ValidationError("Debes especificar el tipo de mascota.")

    class Meta:
        db_table = 'Beneficiario'
        verbose_name = 'Beneficiario'
        verbose_name_plural = 'Beneficiarios'

    def __str__(self):
        return f"{self.nombre_completo} (Titular: {self.titular})"