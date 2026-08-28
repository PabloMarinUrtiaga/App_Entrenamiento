from django.shortcuts import render

# Create your views here.

from rest_framework import generics, permissions
from .models import AthleteProfile
from .serializers import AthleteProfileSerializer, AthleteProfileCoachSerializer


class MyAthleteProfileView(generics.RetrieveUpdateAPIView):
    # El propio deportista ve/edita SU perfil (posición, sub-posición, peso, altura)
    serializer_class = AthleteProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.athlete_profile


class MyAthletesListView(generics.ListAPIView):
    # El entrenador ve la lista de TODOS sus deportistas asignados
    serializer_class = AthleteProfileCoachSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return AthleteProfile.objects.filter(coach=self.request.user)


class AthleteProfileDetailView(generics.RetrieveUpdateAPIView):
    # El entrenador consulta/edita el perfil de UN deportista puntual (si es suyo)
    serializer_class = AthleteProfileCoachSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = AthleteProfile.objects.all()

    def get_queryset(self):
        # Filtra de entrada: solo deja ver perfiles de deportistas que le pertenecen a este coach
        return AthleteProfile.objects.filter(coach=self.request.user)