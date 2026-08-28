from django.shortcuts import render

# Create your views here.

from rest_framework import generics, permissions
from accounts.permissions import IsCoach
from .models import Attendance
from .serializers import AttendanceSerializer


class MyAttendanceView(generics.ListCreateAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Attendance.objects.filter(athlete=self.request.user)

    def perform_create(self, serializer):
        serializer.save(athlete=self.request.user, registered_by=self.request.user)


class AttendanceListCreateView(generics.ListCreateAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [IsCoach]

    def get_queryset(self):
        return Attendance.objects.filter(athlete__athlete_profile__coach=self.request.user)

    def perform_create(self, serializer):
        serializer.save(registered_by=self.request.user)