from django.urls import path
from .views import landing, coach_dashboard, athlete_dashboard

urlpatterns = [
    path("", landing, name="landing"),
    path("coach/", coach_dashboard, name="coach-dashboard"),
    path("athlete/", athlete_dashboard, name="athlete-dashboard"),
]