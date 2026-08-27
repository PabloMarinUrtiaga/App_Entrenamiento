from django.db import models
from django.conf import settings
from exercises.models import Exercise
# Create your models here.

class Result(models.Model):
    # Registro de rendimiento real de un deportista en un ejercicio puntual, en una fecha puntual
    athlete = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="results",
        limit_choices_to={"role": "athlete"},
    )
    exercise = models.ForeignKey(
        Exercise, on_delete=models.CASCADE, related_name="results"
    )
    date = models.DateField(auto_now_add=True)

    # Métricas de rendimiento — todas opcionales, porque no todos los ejercicios
    # se miden con lo mismo (algunos por reps/peso, otros por tiempo o distancia)
    reps = models.PositiveIntegerField(null=True, blank=True)
    weight_kg = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    duration_seconds = models.PositiveIntegerField(null=True, blank=True)
    distance_m = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.athlete} - {self.exercise} ({self.date})"


class CoachNote(models.Model):
    # Nota de texto que el entrenador le deja a un deportista puntual
    athlete = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="coach_notes",
        limit_choices_to={"role": "athlete"},
    )
    coach = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="written_notes",
        limit_choices_to={"role": "coach"},
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Nota a {self.athlete} ({self.created_at.date()})"