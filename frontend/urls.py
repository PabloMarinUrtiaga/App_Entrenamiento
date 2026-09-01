from django.urls import path
from .views import landing, coach_dashboard, athlete_dashboard, athlete_detail, exercise_management

urlpatterns = [
    path("", landing, name="landing"),
    path("coach/", coach_dashboard, name="coach-dashboard"),
    path("athlete/", athlete_dashboard, name="athlete-dashboard"),
    path("coach/athletes/<int:athlete_id>/", athlete_detail, name="athlete-detail"),
    path("coach/exercises/", exercise_management, name="exercise-management"),
]