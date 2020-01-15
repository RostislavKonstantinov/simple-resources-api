from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from users.test_utils import UserClientMixin, random_string
from .models import Resource, UserQuota


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
    @property
    def resources_path(self):
        return reverse('resources')

    def get_resource_path(self, pk):
        return reverse('resource', kwargs=dict(pk=pk))

    def test_list_resources_unauthorized(self):
        response = self.client.get(self.resources_path)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_resources_user(self):
        Resource.objects.create(user=self.user, name=random_string())
        Resource.objects.create(user=self.admin, name=random_string())
        response = self.user_client.get(self.resources_path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), Resource.objects.filter(user=self.user).count())

    def test_list_resources_admin(self):
        Resource.objects.create(user=self.user, name=random_string())
        Resource.objects.create(user=self.admin, name=random_string())
        response = self.admin_client.get(self.resources_path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), Resource.objects.all().count())

    def test_list_filtered_resources_admin(self):
        Resource.objects.create(user=self.user, name=random_string())
        Resource.objects.create(user=self.admin, name=random_string())
        response = self.admin_client.get(self.resources_path, data=dict(user_id=self.user.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), Resource.objects.filter(user=self.user).count())

    def test_create_resource_user(self):
        name = random_string()
        response = self.user_client.post(self.resources_path, dict(name=name))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['name'], name)
        self.assertEqual(response.json()['user_id'], self.user.pk)

    def test_create_resource_admin(self):
        name = random_string()
        response = self.admin_client.post(self.resources_path, dict(name=name))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['name'], name)
        self.assertEqual(response.json()['user_id'], self.admin.pk)

    def test_create_resource_user_for_another_user(self):
        name = random_string()
        response = self.user_client.post(self.resources_path, dict(name=name, user_id=self.admin.pk))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['name'], name)
        self.assertEqual(response.json()['user_id'], self.user.pk)

    def test_create_resource_admin_for_another_user(self):
        name = random_string()
        response = self.admin_client.post(self.resources_path, dict(name=name, user_id=self.user.pk))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['name'], name)
        self.assertEqual(response.json()['user_id'], self.user.pk)

    def test_create_resource_user_if_limit_is_exceeded(self):
        self.user.quota.limit = 0
        self.user.quota.save()
        response = self.user_client.post(self.resources_path, dict(name=random_string()))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_resource_admin_if_limit_is_exceeded(self):
        self.user.quota.limit = 0
        self.user.quota.save()
        response = self.admin_client.post(self.resources_path, dict(name=random_string(), user_id=self.user.pk))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_resource_user(self):
        name = random_string()
        resource = Resource.objects.create(user=self.user, name=name)
        response = self.user_client.get(self.get_resource_path(resource.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['id'], resource.pk)
        self.assertEqual(response.json()['name'], name)
        self.assertEqual(response.json()['user_id'], self.user.pk)

    def test_get_resource_admin(self):
        name = random_string()
        resource = Resource.objects.create(user=self.user, name=name)
        response = self.admin_client.get(self.get_resource_path(resource.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['id'], resource.pk)
        self.assertEqual(response.json()['name'], name)
        self.assertEqual(response.json()['user_id'], self.user.pk)

    def test_get_resource_user_for_another_user(self):
        resource = Resource.objects.create(user=self.random_user(), name=random_string())
        response = self.user_client.get(self.get_resource_path(resource.pk))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_resource_user(self):
        resource = Resource.objects.create(user=self.user, name=random_string())
        response = self.user_client.delete(self.get_resource_path(resource.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Resource.objects.filter(pk=resource.pk).exists())

    def test_delete_resource_admin(self):
        resource = Resource.objects.create(user=self.user, name=random_string())
        response = self.admin_client.delete(self.get_resource_path(resource.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Resource.objects.filter(pk=resource.pk).exists())

    def test_delete_resource_user_for_another_user(self):
        resource = Resource.objects.create(user=self.random_user(), name=random_string())
        response = self.user_client.delete(self.get_resource_path(resource.pk))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
