from django.shortcuts import render

# Create your views here.

from rest_framework import generics, permissions
from .models import Routine, RoutineExercise, RoutineAssignment
from .serializers import RoutineSerializer, RoutineExerciseSerializer, RoutineAssignmentSerializer


class RoutineListCreateView(generics.ListCreateAPIView):
    queryset = Routine.objects.all()
    serializer_class = RoutineSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class RoutineDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Routine.objects.all()
    serializer_class = RoutineSerializer
    permission_classes = [permissions.IsAuthenticated]


class RoutineExerciseListCreateView(generics.ListCreateAPIView):
    # Agrega/lista ejercicios DENTRO de una rutina puntual
    serializer_class = RoutineExerciseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return RoutineExercise.objects.filter(routine_id=self.kwargs["routine_id"])

    def perform_create(self, serializer):
        serializer.save(routine_id=self.kwargs["routine_id"])


class MyRoutineAssignmentsView(generics.ListAPIView):
    # El deportista ve SUS rutinas asignadas
    serializer_class = RoutineAssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return RoutineAssignment.objects.filter(athlete=self.request.user)


class RoutineAssignmentListCreateView(generics.ListCreateAPIView):
    # El entrenador asigna rutinas a deportistas
    queryset = RoutineAssignment.objects.all()
    serializer_class = RoutineAssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(assigned_by=self.request.user)


class RoutineAssignmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    # El entrenador modifica/quita una asignación puntual
    queryset = RoutineAssignment.objects.all()
    serializer_class = RoutineAssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]