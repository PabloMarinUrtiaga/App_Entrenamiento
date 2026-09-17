from django import forms
from .models import CoachNote, Result


class CoachNoteForm(forms.ModelForm):
    class Meta:
        model = CoachNote
        fields = ["athlete", "text"]

class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ["exercise", "reps", "weight_kg", "duration_seconds", "distance_m"]

class CoachResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ["athlete", "exercise", "reps", "weight_kg", "duration_seconds", "distance_m"]