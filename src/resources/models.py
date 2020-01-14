from django.db import models

from users.models import User


class UserQuota(models.Model):
    user = models.OneToOneField(
        User, primary_key=True, related_name='quota', on_delete=models.CASCADE, null=False, editable=False
    )
    limit = models.PositiveIntegerField(null=True, default=None)


class Resource(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, editable=False, null=False, related_name='resources')
    name = models.CharField(max_length=200, null=False, blank=False)
