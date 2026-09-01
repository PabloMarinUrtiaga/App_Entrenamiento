# Create your views here.

from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer

class MeView(generics.RetrieveUpdateAPIView):
    # Devuelve/edita SOLO el perfil del usuario logueado (no una lista de todos)
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class RequestCoachView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        request.user.wants_to_be_coach = True
        request.user.save()
        return Response({"wants_to_be_coach": True})