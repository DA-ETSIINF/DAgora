from django.db import models, transaction
from django.contrib.auth.models import User
import os
from django.db.models.signals import pre_delete, post_delete
from django.dispatch import receiver
from django.conf import settings
from django.core.files.storage import default_storage
import shutil

# Meeting model -> basic atributes and structure of a Meeting
class Meeting(models.Model):
    name = models.CharField(max_length=100, unique = False)
    description = models.TextField(default = ' ')
    date = models.DateField()
    attendees = models.ManyToManyField(User, through='Attendance', related_name = 'meetings')
    creator = models.ForeignKey(User, blank=True, default='', on_delete=models.CASCADE, related_name = 'created_meetings')

    # ToString()
    def __str__(self):
        return self.name

@receiver(pre_delete, sender=Meeting)
def delete_meeting_folder(sender, instance, **kwargs):
    # Get the folder path for the meeting
    folder_path = os.path.join(settings.MEDIA_ROOT, str(instance.name))
    
    # Check if the folder exists
    if default_storage.exists(folder_path):
        # Delete the folder
        shutil.rmtree(folder_path)


# Attendance model -> Links User and Meeting and adds an attribute for if the user is going to attend the meeting
class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name='attendances')
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='attendances')
    attendance = models.BooleanField(default=False) # if the user is going to the meeting or not (true/false)

    # ToString() (Only for better overwiev in admin page)
    def __str__(self):
        return self.meeting.name + ' - ' + self.user.username
    


# File model -> Creates a connection between a meeting and the files linked to it, also automatically saves the files in the correct directory when creating a File instance    
def get_file_upload_path(instance,filename):
    meeting_name = instance.meeting.name
    upload_path = os.path.join(settings.MEDIA_ROOT, f"{meeting_name}", filename)
    return upload_path

class File(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE,related_name='files')
    file = models.FileField(upload_to=get_file_upload_path, max_length=300)
    title = models.CharField(max_length = 300, blank=True)

    def save(self, *args, **kwargs):
        self.title = os.path.basename(self.file.name)
        super().save(*args,**kwargs)

    def __str__(self):
        return str(self.title)

@receiver(pre_delete, sender=File)
def delete_file(sender, instance, **kwargs):
    # Delete the associated file when the File instance is deleted
    if instance.file:
        # Delete the file from the storage
        instance.file.delete(False) # False so the instance.file.delete() function doesnt trigger an instance.save(), which we dont want since we are deleting it
    



