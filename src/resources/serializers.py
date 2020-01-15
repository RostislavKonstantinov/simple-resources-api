from typing import Dict, Any, Optional

from django.db import transaction
from django.utils.functional import cached_property
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from users.models import User
from .models import UserQuota, Resource


class UserQuotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserQuota
        fields = ('user_id', 'limit')

    def _validate_limit(self, limit: Optional[int], user: User):
        UserQuota.objects.select_for_update().get(user=user)
        if limit is None:
            return

        user_resources_count = user.resources.count()
        if user_resources_count > limit:
            raise serializers.ValidationError({'limit': [f'Cannot be less than current resources count. '
                                                         f'Current resources count is {user_resources_count}.']})

    @transaction.atomic()
    def update(self, instance: UserQuota, validated_data: Dict[str, Any]) -> UserQuota:
        if 'limit' in validated_data:
            self._validate_limit(validated_data['limit'], instance.user)
        return super().update(instance, validated_data)


class ResourceSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        source='user',
        queryset=User.objects.all(),
        default=serializers.CreateOnlyDefault(serializers.CurrentUserDefault()),
    )

    @cached_property
    def request_user(self) -> User:
        return self.context['request'].user

    class Meta:
        model = Resource
        fields = ('id', 'user_id', 'name')

    @transaction.atomic()
    def create(self, validated_data: Dict[str, Any]) -> Resource:
        user = validated_data['user'] if self.request_user.is_staff else self.request_user
        quota = UserQuota.objects.select_for_update().get(user=user)
        if quota.limit is not None and user.resources.count() >= quota.limit:
            raise PermissionDenied(f'Resources quota is exceeded. Current limit is {quota.limit}.')
        return super().create(validated_data)
