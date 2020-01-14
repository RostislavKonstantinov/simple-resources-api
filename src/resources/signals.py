from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import User
from .models import UserQuota


@receiver(post_save, sender=User, dispatch_uid="add_user_quota_by_user_created")
def user_saved(sender, instance: User, created: bool, **kwargs):
    if created:
        UserQuota.objects.create(user=instance)
