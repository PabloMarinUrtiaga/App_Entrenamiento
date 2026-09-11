from django.db import models
from django.conf import settings

# Create your models here.
class Exercise(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="exercises/", null=True, blank=True)
    youtube_url = models.URLField(blank=True)  # link que reenvía a un video de YouTube
    catalog_slug = models.CharField(max_length=100, blank=True)  # slug de workout-guide, si se usó una ilustración del catálogo

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_exercises",
        limit_choices_to={"role": "coach"},
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def illustration_static_path(self):
        if self.catalog_slug:
            return f"exercises/workout_guide/{self.catalog_slug}.svg"
        return ""

    def __str__(self):
        return self.name