from django.shortcuts import render

# Create your views here.

from rest_framework import generics, permissions
from accounts.permissions import IsCoach
from .models import AthleteProfile
from .serializers import AthleteProfileSerializer, AthleteProfileCoachSerializer


class MyAthleteProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = AthleteProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.athlete_profile


class MyAthletesListView(generics.ListAPIView):
    serializer_class = AthleteProfileCoachSerializer
    permission_classes = [IsCoach]

    def get_queryset(self):
        return AthleteProfile.objects.filter(coach=self.request.user)


class AthleteProfileDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = AthleteProfileCoachSerializer
    permission_classes = [IsCoach]

    def get_queryset(self):
        return AthleteProfile.objects.filter(coach=self.request.user)