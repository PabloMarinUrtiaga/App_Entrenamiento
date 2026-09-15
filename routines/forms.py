from django import forms
from .models import Routine, RoutineExercise, RoutineAssignment


class RoutineForm(forms.ModelForm):
    class Meta:
        model = Routine
        fields = ["name", "description"]


class RoutineExerciseForm(forms.ModelForm):
    class Meta:
        model = RoutineExercise
        fields = ["exercise", "sets", "reps", "notes"]


class RoutineAssignmentForm(forms.ModelForm):
    class Meta:
        model = RoutineAssignment
        fields = ["athlete"]