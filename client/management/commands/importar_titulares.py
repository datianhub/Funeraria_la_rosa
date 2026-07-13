"""
Comando de Django management para importar titulares_2026.csv al modelo Titular.

Uso:
    1) Copia este archivo a:  <tu_app>/management/commands/importar_titulares.py
       (crea las carpetas management/ y management/commands/ con un __init__.py
       vacío en cada una, si no existen).
    2) Copia titulares_2026.csv a la raíz del proyecto (o ajusta la ruta abajo).
    3) Ejecuta:
           python manage.py importar_titulares

NOTA IMPORTANTE sobre 'fecha_ingreso':
    El modelo define fecha_ingreso con auto_now_add=True. Django ignora
    CUALQUIER valor que le pases a ese campo en el momento de crear el objeto
    (tanto con .save() como con bulk_create): siempre lo pisa con la fecha/hora
    actual. Por eso, para dejar la fecha real del Excel (columna FECHA), el
    truco es:
        a) crear el registro normalmente (auto_now_add pone la fecha de hoy)
        b) hacer un UPDATE posterior con .update(), que SÍ respeta el valor
           que le des porque no pasa por la lógica de auto_now_add.
    Este script ya hace eso automáticamente.
"""
import csv
from datetime import datetime

from django.core.management.base import BaseCommand
from django.db import transaction

from client.models import Titular  # <-- AJUSTA 'tu_app' al nombre real de tu app

CSV_PATH = "titulares_2026.csv"  # ajusta la ruta si es necesario


class Command(BaseCommand):
    help = "Importa titulares desde titulares_2026.csv (generado con pandas)"

    def handle(self, *args, **options):
        creados, saltados, errores = 0, 0, []

        with open(CSV_PATH, newline="", encoding="utf-8-sig") as f:
            lector = csv.DictReader(f)
            filas = list(lector)

        with transaction.atomic():
            for fila in filas:
                numero_contrato_raw = fila["numero_contrato"].strip()
                cedula_raw = fila["cedula"].strip()

                # Registros que necesitan decisión manual (ej. contrato '91/92')
                # no se importan automáticamente; quedan reportados al final.
                if not numero_contrato_raw.isdigit() or not cedula_raw.isdigit():
                    errores.append(
                        f"  - {fila.get('nombre_completo_original','')}: "
                        f"contrato='{numero_contrato_raw}' cedula='{cedula_raw}' "
                        f"(no numérico, revisar manualmente)"
                    )
                    saltados += 1
                    continue

                numero_contrato = int(numero_contrato_raw)
                cedula = int(cedula_raw)

                if Titular.objects.filter(cedula=cedula).exists() or \
                   Titular.objects.filter(numero_contrato=numero_contrato).exists():
                    saltados += 1
                    continue

                titular = Titular.objects.create(
                    cedula=cedula,
                    numero_contrato=numero_contrato,
                    nombre=fila["nombre"],
                    apellido=fila["apellido"],
                    sexo=fila["sexo"],
                    edad=int(fila["edad"]) if fila["edad"].strip() else None,
                    estado_civil=fila["estado_civil"] or None,
                    ocupacion=fila["ocupacion"] or None,
                    direccion=fila["direccion"],
                    telefono=int(fila["telefono"]),
                    plan_activo=fila["plan_activo"].strip().lower() == "true",
                )

                # Sobrescribe fecha_ingreso (auto_now_add) con la fecha real del Excel
                if fila["fecha_ingreso"].strip():
                    fecha = datetime.strptime(fila["fecha_ingreso"].strip(), "%Y-%m-%d").date()
                    Titular.objects.filter(pk=titular.pk).update(fecha_ingreso=fecha)

                creados += 1

        self.stdout.write(self.style.SUCCESS(f"Titulares creados: {creados}"))
        self.stdout.write(f"Titulares saltados (ya existían o datos inválidos): {saltados}")
        if errores:
            self.stdout.write(self.style.WARNING("Revisar manualmente:"))
            for e in errores:
                self.stdout.write(e)