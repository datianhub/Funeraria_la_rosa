from datetime import date
from decimal import Decimal
from django.utils import timezone
from django.db import models

from client.models import Titular
# Create your models here.

class Pago(models.Model):
    titular = models.ForeignKey(Titular, on_delete=models.CASCADE)
    monto_cargos_unicos = models.DecimalField(max_digits=10, decimal_places=2)
    monto_total_a_pagar = models.DecimalField(max_digits=10, decimal_places=2)
    monto_mensual_tarifa = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_ultimo_pago = models.DateTimeField(auto_now_add=True)
    proximo_pago = models.DateField(null=True, blank=True, verbose_name="Proximo Pago")
    plan_vencido = models.BooleanField(default=False)

    class Meta:
        db_table = 'Pago'
        verbose_name = 'pago'
        verbose_name_plural = 'Pagos'

    def guardar_totales(self):
        self.monto_total_a_pagar = self.monto_mensual_tarifa + self.monto_cargos_unicos
        self.save()

    @property
    def esta_vencido(self):
        if not self.proximo_pago:
            return False
        return timezone.localdate() > self.proximo_pago

    def __str__(self):
        return f"Titular : {self.titular}, Monto: {self.monto_total_a_pagar}, Plan vencido: {self.plan_vencido} "


class Factura(models.Model):
    ESTADO_GENERADA = 'generada'
    ESTADO_ANULADA = 'anulada'

    ESTADO_CHOICES = [
        (ESTADO_GENERADA, 'Generada'),
        (ESTADO_ANULADA, 'Anulada'),
    ]

    MESES = [
        '',
        'Enero',
        'Febrero',
        'Marzo',
        'Abril',
        'Mayo',
        'Junio',
        'Julio',
        'Agosto',
        'Septiembre',
        'Octubre',
        'Noviembre',
        'Diciembre',
    ]

    pago = models.ForeignKey(Pago, on_delete=models.CASCADE, related_name='facturas')
    titular = models.ForeignKey(Titular, on_delete=models.CASCADE, related_name='facturas')
    numero = models.CharField(max_length=30, unique=True, blank=True)
    periodo_anio = models.PositiveSmallIntegerField()
    periodo_mes = models.PositiveSmallIntegerField()
    monto_mensual_tarifa = models.DecimalField(max_digits=10, decimal_places=2)
    monto_cargos_unicos = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default=ESTADO_GENERADA)

    class Meta:
        db_table = 'Factura'
        verbose_name = 'Factura'
        verbose_name_plural = 'Facturas'
        ordering = ['-fecha_emision']
        constraints = [
            models.UniqueConstraint(
                fields=['pago', 'periodo_anio', 'periodo_mes'],
                name='factura_unica_por_pago_y_periodo',
            )
        ]

    @property
    def periodo_fecha(self):
        return date(self.periodo_anio, self.periodo_mes, 1)

    @property
    def periodo_nombre(self):
        return f"{self.MESES[self.periodo_mes]} {self.periodo_anio}"

    def save(self, *args, **kwargs):
        if not self.monto_total:
            self.monto_total = self.monto_mensual_tarifa + self.monto_cargos_unicos

        if not self.numero and self.pago_id:
            self.numero = f"FAC-{self.periodo_anio}{self.periodo_mes:02d}-{self.pago_id:06d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.numero or 'Factura'} - {self.titular} - {self.periodo_nombre}"
