from rest_framework import serializers
from .models import Result, CoachNote


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = (
            "id", "athlete", "exercise", "date",
            "reps", "weight_kg", "duration_seconds", "distance_m",
        )
        read_only_fields = ("date",)


class CoachNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoachNote
        fields = ("id", "athlete", "coach", "text", "created_at")
        read_only_fields = ("coach", "created_at")