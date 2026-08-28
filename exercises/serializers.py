from rest_framework import serializers
from .models import Exercise


class ExerciseSerializer(serializers.ModelSerializer):
    # Usado por el Deportista: solo lectura de los ejercicios existentes
    class Meta:
        model = Exercise
        fields = ("id", "name", "description", "image", "youtube_url", "created_by", "created_at")
        read_only_fields = fields