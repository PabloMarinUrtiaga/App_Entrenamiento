from django.urls import path
from .views import MyAthleteProfileView, MyAthletesListView, AthleteProfileDetailView

urlpatterns = [
    path("me/", MyAthleteProfileView.as_view(), name="my-athlete-profile"),
    path("athletes/", MyAthletesListView.as_view(), name="my-athletes"),
    path("athletes/<int:pk>/", AthleteProfileDetailView.as_view(), name="athlete-detail"),
]