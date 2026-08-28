from django.shortcuts import render

# Create your views here.

from rest_framework import generics, permissions
from accounts.permissions import IsCoach
from .models import Result, CoachNote
from .serializers import ResultSerializer, CoachNoteSerializer


class MyResultsView(generics.ListCreateAPIView):
    serializer_class = ResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Result.objects.filter(athlete=self.request.user)

    def perform_create(self, serializer):
        serializer.save(athlete=self.request.user)


class ResultListCreateView(generics.ListCreateAPIView):
    serializer_class = ResultSerializer
    permission_classes = [IsCoach]

    def get_queryset(self):
        return Result.objects.filter(athlete__athlete_profile__coach=self.request.user)


class ResultDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ResultSerializer
    permission_classes = [IsCoach]

    def get_queryset(self):
        return Result.objects.filter(athlete__athlete_profile__coach=self.request.user)


class MyCoachNotesView(generics.ListAPIView):
    serializer_class = CoachNoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CoachNote.objects.filter(athlete=self.request.user)


class CoachNoteListCreateView(generics.ListCreateAPIView):
    serializer_class = CoachNoteSerializer
    permission_classes = [IsCoach]

    def get_queryset(self):
        return CoachNote.objects.filter(coach=self.request.user)

    def perform_create(self, serializer):
        serializer.save(coach=self.request.user)