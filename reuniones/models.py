from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.utils import timezone

# for deletion of saved files when deleting a 'Document' class
from django.db.models.signals import pre_delete
from django.dispatch import receiver
import os


# Create your models here.



# Document Upload -> Has to be over Reunion as Reunion utilices it as an attribute

class Document(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='documents/', max_length = 750)

    def __str__(self):
        return self.title

# Makes file get deleted when deleting its 'Document' object -> usefull so we can delete files during code instead of having to do it manually
@receiver(pre_delete, sender=Document)
def delete_document_file(sender, instance, **kwargs):
    # Delete the file when the corresponding Document object is deleted
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)


class TempDocument(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='temp/documents/', max_length = 750)
    creation_date = models.DateTimeField()

    def __str__(self):
        return self.title
    

    #Ahora hay que ver cuando cuando correrlo 
    #Run function everytime someone visits home? Maybe not the most efficient way but should work
    def delete_odl_docs():
        limit = timezone.now() - timezone.timedelta(days=1)
        old_docs = TempDocument.objects.filter(creation_date__lt=limit)
        old_docs.delete()


    
@receiver(pre_delete, sender=TempDocument)
def delete_temp_document_file(sender, instance, **kwargs):
    # Delete the file when the corresponding TempDocument object is deleted
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)



#Reunion model -> basic attributes of the reunion
# Time attribute?
class Reunion(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(default = ' ')
    date = models.DateField()
    attendees = models.ManyToManyField(User, through='Attendance', related_name='meetings')

    documents = models.ManyToManyField(Document, related_name='reunions', blank=True)

    creator = models.ForeignKey(User, blank=True, default='', on_delete=models.CASCADE, related_name='createdReunions')


    # ToString() override 
    # So when I render/print a reunion the name comes up instead of an attribute array -> userSelectionForm
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











