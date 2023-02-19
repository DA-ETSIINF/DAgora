from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class UserProfile(models.Model):

    # OneToOneField to User so there is exactly always one "profile" per user and so they are linked
    # Cascade so the CustomProfile gets deleted when the user is deleted
    # This basically makes the UserProfile class an extension of the User attributes
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    clase = models.CharField(max_length=10, null = True, blank = True)
    role = models.CharField(max_length=150, null = True, blank = True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user = instance)


