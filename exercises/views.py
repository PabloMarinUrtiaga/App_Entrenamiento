from django.shortcuts import render

# Create your views here.

from rest_framework import generics, permissions
from .models import Exercise
from .serializers import ExerciseSerializer


class ExerciseListCreateView(generics.ListCreateAPIView):
    # GET: cualquier usuario autenticado ve la lista de ejercicios
    # POST: solo lo va a poder usar un Entrenador (por ahora sin restringir, lo ajustamos con permisos custom después)
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ExerciseDetailView(generics.RetrieveUpdateDestroyAPIView):
    # Ver, editar o borrar UN ejercicio puntual
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [permissions.IsAuthenticated]