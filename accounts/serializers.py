from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    age = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = (
            "id", "username", "first_name", "last_name",
            "email", "role", "birth_date", "age", "is_approved",
        )
        read_only_fields = ("role", "is_approved")


class UserApprovalSerializer(serializers.ModelSerializer):
    # Serializer aparte, solo para que un admin/coach apruebe y asigne rol
    class Meta:
        model = User
        fields = ("id", "role", "is_approved")