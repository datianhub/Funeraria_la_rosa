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
    fecha_ingreso = models.DateField(auto_now_add=True)
    plan_activo = models.BooleanField(default=False)

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
    edad_afiliacion = models.PositiveSmallIntegerField(null=True, blank=False)
    edad_actual = models.PositiveSmallIntegerField(null=True, blank=True)
    fecha_afiliacion = models.DateField(auto_now_add=True)
    cobro_edad_aplicado = models.BooleanField(default=False)
    notas = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'Beneficiario'
        verbose_name = 'Beneficiario'
        verbose_name_plural = 'Beneficiarios'

    def __str__(self):
        return f"{self.nombre_completo} (Titular: {self.titular})"
    

class Mascota(models.Model):
    titular = models.ForeignKey(Titular, on_delete=models.CASCADE, related_name='mascotas')
    nombre = models.CharField(max_length=100, blank=True, null=True)
    especie = models.CharField(max_length=50)
    fecha_afiliacion = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'Mascota'
        verbose_name = 'Mascota'
        verbose_name_plural = 'Mascotas'

    def __str__(self):
        return f"Nombre mascota : {self.nombre} ,Especie: {self.especie} , Titular : {self.titular}"