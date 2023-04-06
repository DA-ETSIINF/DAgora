from django import forms
from django.contrib.auth.models import User





# Form not currently being used -> For ajax request i had to manually create the form html
class ReunionForm(forms.Form):
    my_name = forms.CharField(label='Name of the Reunion:', max_length=100)
    my_date = forms.DateField(label='Date', widget=forms.DateInput(attrs = {'type': 'date'}))
    my_description = forms.CharField(label='Description', widget=forms.Textarea)








    

