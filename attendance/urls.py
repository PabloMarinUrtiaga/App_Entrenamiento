from django.urls import path
from .views import MyAttendanceView, AttendanceListCreateView

urlpatterns = [
    path("mine/", MyAttendanceView.as_view(), name="my-attendance"),
    path("", AttendanceListCreateView.as_view(), name="attendance-list"),
]