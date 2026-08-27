from django.db import models
from django.conf import settings
# Create your models here.

class Attendance(models.Model):
    # Registro de asistencia diaria: puede cargarlo el propio deportista o el entrenador
    athlete = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="attendances",
        limit_choices_to={"role": "athlete"},
    )
    date = models.DateField(auto_now_add=True)
    registered_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="attendances_registered",
        # quién cargó el registro: el propio deportista o su entrenador
    )

    class Meta:
        ordering = ["-date"]
        unique_together = ("athlete", "date")  # un solo registro de asistencia por día

    def __str__(self):
        return f"{self.athlete} - {self.date}"