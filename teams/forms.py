from django import forms
from .models import AthleteProfile


class AthleteProfileForm(forms.ModelForm):
    class Meta:
        model = AthleteProfile
        fields = ["position", "sub_position", "weight_kg", "height_cm"]
        