from django.shortcuts import render

# Create your views here.

from rest_framework import generics, permissions
from .models import Attendance
from .serializers import AttendanceSerializer

class MyAttendanceView(generics.ListCreateAPIView):
    # El deportista ve y marca SU propia asistencia
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Attendance.objects.filter(athlete=self.request.user)

    def perform_create(self, serializer):
        serializer.save(athlete=self.request.user, registered_by=self.request.user)


class AttendanceListCreateView(generics.ListCreateAPIView):
    # El entrenador ve/marca asistencia de cualquiera de sus deportistas
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(registered_by=self.request.user)