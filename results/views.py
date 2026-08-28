from django.shortcuts import render

# Create your views here.

from rest_framework import generics, permissions
from .models import Result, CoachNote
from .serializers import ResultSerializer, CoachNoteSerializer


class MyResultsView(generics.ListCreateAPIView):
    # El deportista ve y carga SUS resultados
    serializer_class = ResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Result.objects.filter(athlete=self.request.user)

    def perform_create(self, serializer):
        serializer.save(athlete=self.request.user)


class ResultListCreateView(generics.ListCreateAPIView):
    # El entrenador ve/carga resultados de cualquiera de sus deportistas
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    permission_classes = [permissions.IsAuthenticated]


class ResultDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    permission_classes = [permissions.IsAuthenticated]


class MyCoachNotesView(generics.ListAPIView):
    # El deportista ve las notas que le dejó su entrenador (solo lectura)
    serializer_class = CoachNoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CoachNote.objects.filter(athlete=self.request.user)


class CoachNoteListCreateView(generics.ListCreateAPIView):
    # El entrenador crea/lista notas para sus deportistas
    queryset = CoachNote.objects.all()
    serializer_class = CoachNoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(coach=self.request.user)