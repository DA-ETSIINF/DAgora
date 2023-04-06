from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver

from reuniones.models import Role

# Create your models here.


class UserProfile(models.Model):

    # OneToOneField to User so there is exactly always one "profile" per user and so they are linked
    # Cascade so the CustomProfile gets deleted when the user is deleted
    # This basically makes the UserProfile class an extension of the User attributes
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    clase = models.CharField(max_length=10, null = True, blank = True)
    role = models.CharField(max_length=150, null = True, blank = True)
    role2 = models.ManyToManyField(Role, blank=True, default='1')

    def __str__(self):
        return self.user.username
    
    def callable_roles(self):
        roles = []
        callable_roles = []
        for role in self.role2.all():
            roles.append(role)
        
        for role in roles:
            for callableRole in role.callable_roles.all():
                if callableRole not in callable_roles:
                    callable_roles.append(callableRole)
        
        return callable_roles

        
        




@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user = instance)


