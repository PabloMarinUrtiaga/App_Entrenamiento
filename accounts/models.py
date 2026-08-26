from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    class Role(models.TextChoices):
        COACH = "coach", "Entrenador"
        ATHLETE = "athlete", "Deportista"

    role = models.CharField(max_length=30, choices=Role.choices, blank=Role.ATHLETE)

    # Nadie puede operar en el sistema hasta ser aprobado
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(
        "self", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="approved_users"
    )

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"