from rest_framework import serializers
from .models import Attendance


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ("id", "athlete", "date", "registered_by")
        read_only_fields = ("date", "registered_by")