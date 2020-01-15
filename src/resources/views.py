from django.contrib.auth.models import AnonymousUser
from django.db.models import QuerySet
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import GenericViewSet

from .models import UserQuota, Resource
from .serializers import UserQuotaSerializer, ResourceSerializer


class UserQuotaViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin, GenericViewSet):
    permission_classes = (IsAdminUser,)
    serializer_class = UserQuotaSerializer
    queryset = UserQuota.objects.all()
    lookup_url_kwarg = 'pk'
    lookup_field = 'user_id'
    filterset_fields = ('user_id',)


class ResourcesViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    permission_classes = (IsAuthenticated,)
    serializer_class = ResourceSerializer
    queryset = Resource.objects.all()
    filterset_fields = ('user_id',)

    def get_queryset(self) -> QuerySet:
        qs = super().get_queryset()

        if isinstance(self.request.user, AnonymousUser):
            return qs.none()

        if not self.request.user.is_staff:
            return qs.filter(user=self.request.user)

        return qs
