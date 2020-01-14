from typing import Any, Dict

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


class RegistrationSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(
        required=True,
        validators=(UniqueValidator(User.objects.all(), message='User with this email already exists.'),)
    )
    password = serializers.CharField(required=True, validators=(validate_password,), write_only=True)

    def create(self, validated_data: Dict[str, Any]) -> User:
        user = User(email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance: User, validated_data: Dict[str, Any]) -> None:
        raise NotImplementedError()


class AuthTokenSerializer(TokenObtainPairSerializer):
    username_field = User.USERNAME_FIELD


class AccessRefreshTokensSerializer(serializers.Serializer):
    """
    Serializer for login response, used in schema views.
    """
    access = serializers.CharField()
    refresh = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'is_staff')


class MeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name')
