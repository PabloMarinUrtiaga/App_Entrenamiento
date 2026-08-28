from django.urls import path
from .views import (
    RoutineListCreateView, RoutineDetailView, RoutineExerciseListCreateView,
    MyRoutineAssignmentsView, RoutineAssignmentListCreateView, RoutineAssignmentDetailView,
)

urlpatterns = [
    path("", RoutineListCreateView.as_view(), name="routine-list"),
    path("<int:pk>/", RoutineDetailView.as_view(), name="routine-detail"),
    path("<int:routine_id>/exercises/", RoutineExerciseListCreateView.as_view(), name="routine-exercise-list"),
    path("assignments/mine/", MyRoutineAssignmentsView.as_view(), name="my-routine-assignments"),
    path("assignments/", RoutineAssignmentListCreateView.as_view(), name="routine-assignment-list"),
    path("assignments/<int:pk>/", RoutineAssignmentDetailView.as_view(), name="routine-assignment-detail"),
]