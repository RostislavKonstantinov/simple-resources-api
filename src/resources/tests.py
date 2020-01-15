from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from .models import Resource, UserQuota
from users.test_utils import UserClientMixin, random_string


class QuotaTests(UserClientMixin, APITestCase):
    @property
    def quotas_path(self):
        return reverse('users-quota')

    def get_quota_path(self, pk):
        return reverse('user-quota', kwargs=dict(pk=pk))

    def test_quota_signal_on_user_created(self):
        self.assertTrue(self.user.quota.limit is None)

    def test_list_quotas_unauthorized(self):
        response = self.client.get(self.quotas_path)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_quotas_user(self):
        response = self.user_client.get(self.quotas_path)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_quotas_admin(self):
        response = self.admin_client.get(self.quotas_path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.json()) > 0)

    def test_list_filtered_quota_by_user(self):
        user = self.random_user()
        response = self.admin_client.get(self.quotas_path, data=dict(user_id=user.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), UserQuota.objects.filter(user=user).count())

    def test_get_quota_user(self):
        response = self.user_client.get(self.get_quota_path(self.user.pk))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_quota_admin(self):
        response = self.admin_client.get(self.get_quota_path(self.user.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['user_id'], self.user.pk)

    def test_put_quota_user(self):
        limit = 2
        response = self.user_client.put(self.get_quota_path(self.user.pk), dict(limit=limit))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_quota_admin(self):
        limit = 2
        response = self.admin_client.put(self.get_quota_path(self.user.pk), dict(limit=limit))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['user_id'], self.user.pk)
        self.assertEqual(response.json()['limit'], limit)

    def test_set_less_quota_then_resources_count(self):
        user = self.random_user()
        Resource.objects.create(user=user, name=random_string())
        response = self.admin_client.put(self.get_quota_path(user.pk), dict(limit=0))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_set_greater_quota_then_resources_count(self):
        user = self.random_user()
        Resource.objects.create(user=user, name=random_string())
        response = self.admin_client.put(self.get_quota_path(user.pk), dict(limit=2))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_set_equal_quota_to_resources_count(self):
        user = self.random_user()
        Resource.objects.create(user=user, name=random_string())
        response = self.admin_client.put(self.get_quota_path(user.pk), dict(limit=1))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ResourcesTests(UserClientMixin, APITestCase):
    pass
