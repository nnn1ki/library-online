from django.contrib.auth.models import Group, User
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver

from library_service.models.user import UserProfile

# TODO: async??


@receiver(post_migrate)
def create_default_groups(_sender, **kwargs):
    Group.objects.get_or_create(name="Librarian")
    Group.objects.get_or_create(name="Reader")


@receiver(post_save, sender=User)
def create_user_profile(_sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(_sender, instance, **kwargs):
    try:
        instance.profile.save()
    except User.profile.RelatedObjectDoesNotExist:
        UserProfile.objects.create(user=instance)
