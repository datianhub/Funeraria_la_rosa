from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Plan, Titular
from .views import calcular_monto_plan

@receiver(post_save, sender=Plan)
def recalcular_montos_al_actualizar_plan(sender, instance, created, **kwargs):
    """
    Este es el "vigilante" que escucha cuando se guarda un Plan.
    
    Parámetros:
    - sender: El modelo que envía el signal (Plan)
    - instance: La instancia del Plan que se guardó
    - created: True si es un registro nuevo, False si es actualización
    - **kwargs: Otros parámetros opcionales
    """
    
    # Solo ejecutar si es una ACTUALIZACIÓN, no una creación nueva
    if not created:
        print("✓ Plan fue actualizado, recalculando montos...")
        
        # Obtén todos los titulares
        titulares = Titular.objects.all()
        
        # Recalcula para cada titular
        for titular in titulares:
            try:
                calcular_monto_plan(titular.id)
                print(f"✓ Monto recalculado para titular {titular.nombre}")
            except Exception as e:
                print(f"✗ Error recalculando para {titular.nombre}: {e}")