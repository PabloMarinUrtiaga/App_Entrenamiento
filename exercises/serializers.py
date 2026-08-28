from rest_framework import serializers
from .models import Exercise


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ("id", "name", "description", "image", "youtube_url", "created_by", "created_at")
        read_only_fields = ("created_by", "created_at")