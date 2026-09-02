from django.urls import path
from .views import (landing, coach_dashboard, athlete_dashboard,
                    athlete_detail, exercise_management,routine_management,
                    routine_detail, attendance_register, add_note,
                    register_result, my_notes,my_results,
                    mark_attendance, my_profile, request_coach, mark_attendance_htmx
                    )

urlpatterns = [
    path("", landing, name="landing"),
    path("coach/", coach_dashboard, name="coach-dashboard"),
    path("athlete/", athlete_dashboard, name="athlete-dashboard"),
    path("coach/athletes/<int:athlete_id>/", athlete_detail, name="athlete-detail"),
    path("coach/exercises/", exercise_management, name="exercise-management"),
    path("coach/routines/", routine_management, name="routine-management"),
    path("coach/routines/<int:routine_id>/", routine_detail, name="routine-detail"),
    path("coach/attendance/", attendance_register, name="attendance-register"),
    path("coach/notes/", add_note, name="add-note"),
    path("results/register/", register_result, name="register-result"),
    path("results/mine/", my_results, name="my-results"),
    path("attendance/mark/", mark_attendance, name="mark-attendance"),
    path("notes/mine/", my_notes, name="my-notes"),
    path("profile/", my_profile, name="my-profile"),
    path("request-coach/", request_coach, name="request-coach-page"),
    path("coach/attendance/mark/<int:athlete_id>/", mark_attendance_htmx, name="mark-attendance-htmx"),
]