from django import forms
from .models import CoachNote


class CoachNoteForm(forms.ModelForm):
    class Meta:
        model = CoachNote
        fields = ["athlete", "text"]