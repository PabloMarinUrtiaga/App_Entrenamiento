from django.db import models
from django.conf import settings
from exercises.models import Exercise
# Create your models here.

class Routine(models.Model):
    # Plantilla de rutina creada por un entrenador, reutilizable entre deportistas
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_routines",
        limit_choices_to={"role": "coach"},
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class RoutineExercise(models.Model):
    # Tabla intermedia: qué ejercicios componen una rutina, en qué orden y con qué carga
    routine = models.ForeignKey(
        Routine, on_delete=models.CASCADE, related_name="routine_exercises"
    )
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)
    sets = models.PositiveIntegerField(null=True, blank=True)
    reps = models.PositiveIntegerField(null=True, blank=True)
    notes = models.CharField(max_length=255, blank=True)  # ej: "3x15 con pelota medicinal"

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.routine} - {self.exercise} (#{self.order})"

class RoutineAssignment(models.Model):
    # Asignación de una rutina a un deportista. El entrenador puede modificarla o cambiarla cuando quiera.
    routine = models.ForeignKey(
        Routine, on_delete=models.CASCADE, related_name="assignments"
    )
    athlete = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="routine_assignments",
        limit_choices_to={"role": "athlete"},
    )
    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="assigned_routines",
        limit_choices_to={"role": "coach"},
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.routine} -> {self.athlete}"
    
