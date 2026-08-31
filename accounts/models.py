from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date

# Create your models here.

class User(AbstractUser):
    class Role(models.TextChoices):
        COACH = "coach", "Entrenador"
        ATHLETE = "athlete", "Deportista"

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.ATHLETE)
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(
        "self", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="approved_users"
    )

    # El usuario pide ser Entrenador, pero sigue operando como Deportista hasta que se apruebe
    wants_to_be_coach = models.BooleanField(default=False)

    birth_date = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.role == self.Role.ATHLETE:
            self.is_approved = True
        super().save(*args, **kwargs)

    def approve_as_coach(self, approved_by):
        # Vos usás esto para aprobar: recién ACÁ el rol pasa a coach de verdad
        self.role = self.Role.COACH
        self.is_approved = True
        self.wants_to_be_coach = False
        self.approved_by = approved_by
        self.save()

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