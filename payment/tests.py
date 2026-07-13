from datetime import date
from decimal import Decimal

from django.test import TestCase

from client.models import Titular
from payment.models import Pago
from payment.services import generar_factura_para_pago, obtener_siguiente_periodo_pago


class FacturaServiceTests(TestCase):
    def setUp(self):
        self.titular = Titular.objects.create(
            cedula=123456,
            numero_contrato=1001,
            nombre='Maria',
            apellido='Rosa',
            sexo='F',
            direccion='Calle 1',
            telefono=3001234567,
        )
        Titular.objects.filter(pk=self.titular.pk).update(fecha_ingreso=date(2026, 5, 20))
        self.titular.refresh_from_db()
        self.pago = Pago.objects.create(
            titular=self.titular,
            monto_mensual_tarifa=Decimal('24000.00'),
            monto_cargos_unicos=Decimal('6000.00'),
            monto_total_a_pagar=Decimal('30000.00'),
        )

    def test_obtener_siguiente_periodo_pago_inicia_en_fecha_ingreso(self):
        self.assertEqual(obtener_siguiente_periodo_pago(self.pago), (2026, 5))

    def test_generar_factura_avanza_periodo_y_no_repite_cargos_unicos(self):
        primera_factura, creada = generar_factura_para_pago(self.pago.id)
        self.assertTrue(creada)
        self.assertEqual(primera_factura.periodo_nombre, 'Mayo 2026')
        self.assertEqual(primera_factura.monto_cargos_unicos, Decimal('6000.00'))
        self.assertEqual(primera_factura.monto_total, Decimal('30000.00'))

        self.pago.refresh_from_db()
        self.assertEqual(self.pago.monto_cargos_unicos, Decimal('0.00'))
        self.assertEqual(self.pago.monto_total_a_pagar, Decimal('24000.00'))
        self.assertEqual(obtener_siguiente_periodo_pago(self.pago), (2026, 6))

        segunda_factura, creada = generar_factura_para_pago(self.pago.id)
        self.assertTrue(creada)
        self.assertEqual(segunda_factura.periodo_nombre, 'Junio 2026')
        self.assertEqual(segunda_factura.monto_cargos_unicos, Decimal('0.00'))
        self.assertEqual(segunda_factura.monto_total, Decimal('24000.00'))
