from django.urls import path
from .views import MeView, RequestCoachView

urlpatterns = [
    path("me/", MeView.as_view(), name="me"),
    path("request-coach/", RequestCoachView.as_view(), name="request-coach"),
]