from django.db import models
from django.conf import settings
# Create your models here

class Position(models.TextChoices):
    ARQUERO = "arquero", "Arquero"
    LATERAL = "lateral", "Lateral"
    CENTRAL = "central", "Central"
    EXTREMO = "extremo", "Extremo"
    PIVOT = "pivot", "Pivot"


class AthleteProfile(models.Model):
    # """Datos específicos de un usuario con rol Deportista."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="athlete_profile",
        limit_choices_to={"role": "athlete"},
    )
    coach = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="athletes",
        limit_choices_to={"role": "coach"},
    )
    position = models.CharField(
        max_length=20, choices=Position.choices, blank=True
    )
    sub_position = models.CharField(
        max_length=20, choices=Position.choices, blank=True,
    )
    
    weight_kg = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    height_cm = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )


    def __str__(self):
        return f"{self.user} - {self.get_position_display() or 'sin posición'}"