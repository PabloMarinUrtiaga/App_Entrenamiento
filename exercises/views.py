from django.shortcuts import render

# Create your views here.

from rest_framework import generics
from accounts.permissions import IsCoachOrReadOnly
from .models import Exercise
from .serializers import ExerciseSerializer


class ExerciseListCreateView(generics.ListCreateAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [IsCoachOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ExerciseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [IsCoachOrReadOnly]