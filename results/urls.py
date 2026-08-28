from django.urls import path
from .views import (
    MyResultsView, ResultListCreateView, ResultDetailView,
    MyCoachNotesView, CoachNoteListCreateView,
)

urlpatterns = [
    path("mine/", MyResultsView.as_view(), name="my-results"),
    path("", ResultListCreateView.as_view(), name="result-list"),
    path("<int:pk>/", ResultDetailView.as_view(), name="result-detail"),
    path("notes/mine/", MyCoachNotesView.as_view(), name="my-coach-notes"),
    path("notes/", CoachNoteListCreateView.as_view(), name="coach-note-list"),
]