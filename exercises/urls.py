from django.urls import path
from .views import ExerciseListCreateView, ExerciseDetailView

urlpatterns = [
    path("", ExerciseListCreateView.as_view(), name="exercise-list"),
    path("<int:pk>/", ExerciseDetailView.as_view(), name="exercise-detail"),
]