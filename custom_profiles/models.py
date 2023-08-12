from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver


class Group(models.Model):
    name = models.CharField(max_length=200, unique = True)

    # ToString()
    def __str__(self):
        return self.name
    
    @property
    def get_users(self):
        return User.objects.filter(userprofile__role__group=self).distinct()


class Permission(models.Model):
    name = models.CharField(max_length=200, unique = True)
    groups = models.ManyToManyField(Group)
    # ToString()
    def __str__(self):
        return self.name



# Role -> Role the User has in the organization (ex. President, videpresident)
# Has a name and a list of other Roles it can call to a Meeting
class Role(models.Model):
    name = models.CharField(max_length = 200, unique = True)
    group = models.ManyToManyField(Group)
    permissions = models.ManyToManyField(Permission, related_name='roles', blank=True)

    # ToString()
    def __str__(self):
        return self.name
    
    # Enables us to do get_users on the html code, as it counts as an attribute instead of a function
    # Returns all users which have this role as one of their roles
    @property
    def get_users(self):
        return User.objects.filter(userprofile__role = self)
    


# UserProfile -> Attribute added to standard User model -> basically an addon of extra attributes to the standard user model (accesable with User.uerprofile.attr)
class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #class attribute? ex. 1A, 1M-B, 3T etc.
    role = models.ManyToManyField(Role, blank=True)

    def __str__(self):
        return self.user.username
    
    # returns a querry of groups that can be called by this user
    def callable_groups(self):
        user_roles = self.role.all()
        permissions = set(permission for role in user_roles for permission in role.permissions.all())
        groups = Group.objects.filter(permission__in=permissions).distinct()
        return groups
    
    # returns true if it has at least one group it can call in its permissions, false if there is nobody that can be called
    def can_create_meeting(self):
        return bool(self.callable_groups())

        
        
# When creating an User it creates a matching UserProfile for it
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user = instance)





