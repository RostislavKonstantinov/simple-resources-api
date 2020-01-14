from typing import Any, Type

from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, mixins
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import NOT, IsAuthenticated, SingleOperandHolder, AllowAny, IsAdminUser

from rest_framework.request import Request
from rest_framework.serializers import Serializer
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .models import User
from .serializers import (
    RegistrationSerializer,
    AuthTokenSerializer,
    UserSerializer,
    MeUserSerializer,
    AccessRefreshTokensSerializer
)


class RegisterViewSet(CreateModelMixin, GenericViewSet):
    permission_classes = (SingleOperandHolder(NOT, IsAuthenticated),)
    serializer_class = RegistrationSerializer


class AuthViewSet(GenericViewSet):
    permission_classes = (AllowAny,)
    serializer_class = AuthTokenSerializer

    @swagger_auto_schema(responses={status.HTTP_201_CREATED: AccessRefreshTokensSerializer()})
    def obtain_token(self, request: Request, *args: Any, **kwargs: Any) -> JsonResponse:
        serializer: Serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return JsonResponse(data=serializer.validated_data, status=status.HTTP_201_CREATED)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)

    action2serializer_class = {
        'create': RegistrationSerializer
    }

    def get_serializer_class(self) -> Type[Serializer]:
        return self.action2serializer_class.get(self.action, super().get_serializer_class())


class MeUserViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = MeUserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self) -> User:
        return self.request.user
