from django.db import models
from django.contrib.auth.models import User
from django import forms


# Create your models here.

#Reunion model -> basic attributes of the reunion
# Time attribute?
class Reunion(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(default = ' ')
    date = models.DateField()
    attendees = models.ManyToManyField(User, through='Attendance', related_name='meetings')


    # ToString() override 
    # So when i render/print a reunion the name comes up instead of an attribute array
    def __str__(self):
        return self.name
    

# Attendance model
# Links User and Reunion together and ads a differend asistance attribute for every User for every Reunion
class Attendance(models.Model):
    # on_delete = models.CASCADE makes the Attendance object get automatically deleted whenever either the Reunion or the User get deleted
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reunion = models.ForeignKey(Reunion, on_delete=models.CASCADE, related_name='attendances')
    asistance = models.BooleanField(default = False)

    # ToString() override
    # Only made it so i can have a better overview on the Attendance attributes on the /admin site -> only usefull for developement, but can be useful when fixing bugs
    def __str__(self):
        return self.reunion.name + ' ' + self.user.username

    def get_full_name(self):
        return self.user.get_full_name()








