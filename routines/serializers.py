from rest_framework import serializers
from .models import Routine, RoutineExercise, RoutineAssignment
from exercises.serializers import ExerciseSerializer


class RoutineExerciseSerializer(serializers.ModelSerializer):
    exercise_detail = ExerciseSerializer(source="exercise", read_only=True)

    class Meta:
        model = RoutineExercise
        fields = ("id", "routine", "exercise", "exercise_detail", "order", "sets", "reps", "notes")
        read_only_fields = ("routine",)


class RoutineSerializer(serializers.ModelSerializer):
    # Anida los ejercicios de la rutina para no tener que pedirlos aparte
    routine_exercises = RoutineExerciseSerializer(many=True, read_only=True)

    class Meta:
        model = Routine
        fields = ("id", "name", "description", "created_by", "created_at", "routine_exercises")
        read_only_fields = ("created_by", "created_at")


class RoutineAssignmentSerializer(serializers.ModelSerializer):
    routine_detail = RoutineSerializer(source="routine", read_only=True)

    class Meta:
        model = RoutineAssignment
        fields = ("id", "routine", "routine_detail", "athlete", "assigned_by", "created_at", "updated_at")
        read_only_fields = ("assigned_by", "created_at", "updated_at")