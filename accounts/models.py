from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date

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
    
    birth_date = models.DateField(null=True, blank=True)

    @property
    def age(self):
        # Calcula la edad a partir de birth_date, no la guarda como número fijo
        if not self.birth_date:
            return None
        today = date.today()
        return today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )


    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"