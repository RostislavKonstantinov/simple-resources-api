from typing import Callable

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from .test_utils import UserClientMixin, random_email, random_string
from .models import User


class RegistrationTests(UserClientMixin, APITestCase):
    def test_register(self):
        email = random_email()
        response = self.client.post(reverse('register'), {'email': email, 'password': random_string()})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.json())
        self.assertIn('email', response.json())
        self.assertTrue(User.objects.filter(email=email).exists())

    def test_register_authorized_user(self):
        response = self.user_client.post(self.register_path, {'email': random_email(), 'password': random_string()})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AuthorizationTests(UserClientMixin, APITestCase):
    def test_register_authorized_admin(self):
        response = self.admin_client.post(self.register_path, {'email': random_email(), 'password': random_string()})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_login_unauthorized(self):
        response = self.client.post(self.login_path, {'email': self.user_email, 'password': self.user_password})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_authorized_user(self):
        response = self.user_client.post(self.login_path, {'email': self.user_email, 'password': self.user_password})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_authorized_admin(self):
        response = self.admin_client.post(self.login_path, {'email': self.admin_email, 'password': self.admin_password})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class UsersTests(UserClientMixin, APITestCase):

    @property
    def users_path(self):
        return reverse('users')

    def get_user_path(self, pk):
        return reverse('user', kwargs=dict(pk=pk))

    def test_users_list_unauthorized(self):
        response = self.client.get(self.users_path)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_users_list_admin(self):
        response = self.admin_client.get(self.users_path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.json()) > 0)

    def test_create_users_admin(self):
        email = random_email()
        response = self.admin_client.post(self.users_path, {'email': email, 'password': random_string()})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email=email).exists())
        self.assertIn('id', response.json())
        self.assertIn('email', response.json())

    def test_get_user_admin(self):
        response = self.admin_client.get(self.get_user_path(self.user.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                'id': self.user.id,
                'email': self.user.email,
                'is_staff': self.user.is_staff,
                'first_name': self.user.first_name,
                'last_name': self.user.last_name,
            }
        )

    def _assert_update_method(self, request_method: Callable) -> None:
        first_name = random_string()
        last_name = random_string()
        response = request_method(self.get_user_path(self.user.id),
                                  {'first_name': first_name, 'last_name': last_name, 'email': random_email()})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['first_name'], first_name)
        self.assertEqual(response.json()['last_name'], last_name)
        self.assertEqual(response.json()['email'], self.user_email)

    def test_put_user_admin(self):
        self._assert_update_method(self.admin_client.put)

    def test_patch_user_admin(self):
        self._assert_update_method(self.admin_client.patch)

    def test_delete_user_admin(self):
        response = self.admin_client.delete(self.get_user_path(self.user.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(email=self.user_email).exists())

    def test_users_list_user(self):
        response = self.user_client.get(self.users_path)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_user_user(self):
        response = self.admin_client.get(self.get_user_path(self.user.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_users_user(self):
        response = self.user_client.post(self.users_path)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_user_user(self):
        response = self.user_client.put(self.get_user_path(self.user.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_users_user(self):
        response = self.user_client.patch(self.get_user_path(self.user.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_users_user(self):
        response = self.user_client.delete(self.get_user_path(self.user.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class MeUsersTests(UserClientMixin, APITestCase):

    @property
    def user_path(self):
        return reverse('me-user')

    def test_get_user(self):
        response = self.user_client.get(self.user_path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                'id': self.user.id,
                'email': self.user.email,
                'first_name': self.user.first_name,
                'last_name': self.user.last_name,
            }
        )

    def _assert_update_method(self, request_method: Callable) -> None:
        first_name = random_string()
        last_name = random_string()
        response = request_method(self.user_path,
                                  {'first_name': first_name, 'last_name': last_name, 'email': random_email()})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['first_name'], first_name)
        self.assertEqual(response.json()['last_name'], last_name)
        self.assertEqual(response.json()['email'], self.user_email)
        self.assertEqual(response.json()['id'], self.user.id)

    def test_put_user(self):
        self._assert_update_method(self.user_client.put)

    def test_patch_user(self):
        self._assert_update_method(self.user_client.patch)

    def test_delete_user(self):
        response = self.user_client.delete(self.user_path)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
