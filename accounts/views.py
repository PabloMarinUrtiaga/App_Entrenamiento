# Create your views here.

from rest_framework import generics, permissions
from .serializers import UserSerializer

class MeView(generics.RetrieveUpdateAPIView):
    # Devuelve/edita SOLO el perfil del usuario logueado (no una lista de todos)
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user