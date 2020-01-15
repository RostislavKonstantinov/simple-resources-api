from rest_framework import serializers

from users.models import User
from .models import UserQuota, Resource


class UserQuotaSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserQuota
        fields = ('user_id', 'limit')


class ResourceSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        source='user',
        queryset=User.objects.all(),
        default=serializers.CreateOnlyDefault(serializers.CurrentUserDefault()),
    )

    class Meta:
        model = Resource
        fields = ('id', 'user_id', 'name')
