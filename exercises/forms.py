from django import forms
from .models import Exercise
from .catalog import load_catalog


class ExerciseForm(forms.ModelForm):
    catalog_slug = forms.ChoiceField(
        required=False,
        label="Ilustración (opcional)",
        choices=[("", "— Sin ilustración —")] + [(e["slug"], e["name"]) for e in load_catalog()],
    )

    class Meta:
        model = Exercise
        fields = ["name", "description", "image", "youtube_url", "catalog_slug"]