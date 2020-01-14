import random
import string

from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from .models import User


def random_string(n: int = 15) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))


def random_email() -> str:
    return f'{random_string()}@test.com'


class UserClientMixin:
    @property
    def register_path(self):
        return reverse('register')

    @property
    def login_path(self):
        return reverse('login')

    def setUp(self) -> None:
        self.admin_email = random_email()
        self.admin_password = random_string()
        self.admin = self.create_user(self.admin_email, self.admin_password, True)
        self.admin_client = self.get_client(self.admin_email, self.admin_password)

        self.user_email = random_email()
        self.user_password = random_string()
        self.user = self.create_user(self.user_email, self.user_password)
        self.user_client = self.get_client(self.user_email, self.user_password)

    def create_user(self, email: str, password: str, is_staff=False) -> User:
        user = User(email=email, is_staff=is_staff)
        user.set_password(password)
        user.save()
        return user

    def get_client(self, email: str, password: str) -> APIClient:
        client = APIClient()
        response = self.client.post(self.login_path, {'email': email, 'password': password})
        token = response.json()['access']
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        return client
