from rest_framework import serializers
from .models import AthleteProfile


class AthleteProfileSerializer(serializers.ModelSerializer):
    # Para que el propio deportista edite su posición/sub-posición
    position_display = serializers.CharField(source="get_position_display", read_only=True)

    class Meta:
        model = AthleteProfile
        fields = (
            "id", "user", "coach", "position", "sub_position",
            "position_display", "weight_kg", "height_cm",
        )
        read_only_fields = ("user", "coach")


class AthleteProfileCoachSerializer(serializers.ModelSerializer):
    # Para que el entrenador edite CUALQUIER dato de sus deportistas (incluida la asignación de coach)
    class Meta:
        model = AthleteProfile
        fields = (
            "id", "user", "coach", "position", "sub_position",
            "weight_kg", "height_cm",
        )