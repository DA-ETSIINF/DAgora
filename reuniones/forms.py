from django import forms
from django.contrib.auth.models import User





# Form used to get the main reunion data. Maybe i'll add a Time attribute? But maybe it's something thats better communicated on whatsapp
class ReunionForm(forms.Form):
    my_name = forms.CharField(label='Name of the Reunion:', max_length=100)
    my_date = forms.DateField(label='Date', widget=forms.DateInput(attrs = {'type': 'date'}))
    my_description = forms.CharField(label='Description', widget=forms.Textarea)


# to add a searchbar to the UserSelectionForm, which i have to make work on javascript. I dont know how tho, as i think i need JQueery, so i'll leave it here for the future maybe. People can use ctrl + G to search anyways...
class SearchableCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    def __init__(self, search_field=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.search_field = search_field

    def render(self, name, value, attrs=None, renderer=None):
        html = super().render(name, value, attrs=attrs, renderer=renderer)
        search_input = f'<input type="text" class="search-field" data-field="{self.search_field}"/>'
        return search_input + html





# Forms used to choose some Users from between all Users
# Used when creating a Reunion, to choose which users to create an Attendance for

# Ordenado por nombre
class UserSelectionFormName(forms.Form):
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all().order_by('first_name'),
        widget = forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['users'].label_from_instance = self.label_from_instance

    #Esto sirve para que a la hora de imprimir los users en el multiplechoicefield que ponga el 'perfil' del usuario y no su nombre de usuario
    def label_from_instance(self, obj):
        #str() para que siga funcionando todo si nos olvidamos de poner clase, rol o nombre + apellido a algun perfil
        return str(obj.get_full_name()) + ' - ' + str(obj.userprofile.clase) + ' - ' + str(obj.userprofile.role)


# Para que este ordenado la form por role
class UserSelectionFormRole(forms.Form):
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all().order_by('userprofile__role'),
        widget = forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['users'].label_from_instance = self.label_from_instance

    #Esto sirve para que a la hora de imprimir los users en el multiplechoicefield que ponga el 'perfil' del usuario y no su nombre de usuario
    def label_from_instance(self, obj):
        #str() para que siga funcionando todo si nos olvidamos de poner clase, rol o nombre + apellido a algun perfil
        return str(obj.get_full_name()) + ' - ' + str(obj.userprofile.clase) + ' - ' + str(obj.userprofile.role)

# Para que este ordenado la form por clase/curso
class UserSelectionFormClass(forms.Form):
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all().order_by('userprofile__clase'), # Problema es que el orden se fija en el primer caracter, por lo cual si hay mas de dos digitos 10 va antes que 2 --> solo funciona si hay menos de 10 cursos
        widget = forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['users'].label_from_instance = self.label_from_instance

    #Esto sirve para que a la hora de imprimir los users en el multiplechoicefield que ponga el 'perfil' del usuario y no su nombre de usuario
    def label_from_instance(self, obj):
        #str() para que siga funcionando todo si nos olvidamos de poner clase, rol o nombre + apellido a algun perfil
        return str(obj.get_full_name()) + ' - ' + str(obj.userprofile.clase) + ' - ' + str(obj.userprofile.role)




#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# vvv Unused Code vvv maybe for future use?


# code for a form to change the asistance attribute --> i think i will change it for custom buttons, as i can make them change it onClick instead of having to press a submit button
class SingleCheckboxInput(forms.widgets.CheckboxSelectMultiple):
    def render(self, name, value, attrs=None, renderer=None):
        attrs['onclick'] = "document.getElementById('id_%s_0').checked=false; document.getElementById('id_%s_1').checked=false; this.checked=true" % (name, name)
        return super().render(name, value, attrs, renderer)


class ChangeAsistanceForm(forms.Form):
    asistance = forms.MultipleChoiceField(
        widget=SingleCheckboxInput,
        choices=((True, 'True'), (False, 'False')),
        required=True,
    )
    

