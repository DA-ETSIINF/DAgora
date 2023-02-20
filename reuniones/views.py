from django.shortcuts import render, redirect
from .models import Reunion, Attendance
from custom_profiles.models import UserProfile
from .forms import ReunionForm, UserSelectionFormName, UserSelectionFormRole, UserSelectionFormClass, ChangeAsistanceForm
from django.contrib.auth.models import User
from django.http import JsonResponse #JQuery AJAX requests


# View para la página principal
def main(request):
    if request.user.is_authenticated == False:
        return redirect('/accounts/login')
    user = request.user
    reunion_list = Reunion.objects.all()

    context = {
        'user' : user,
        'reunion_list' : reunion_list,
        }

    return render(request, 'home.html', context)

# View para cuando se mira la información de la reunión y se cambia la asistencia del usuario
def reunionAsistances(request, reunion_name):

    #checks if user is authenticated -> if not -> redirect to login
    if request.user.is_authenticated == False:
        return redirect('/accounts/login')


    reunion = Reunion.objects.get(name = reunion_name)


    # el order.by es para que no se coloquen en orden de creación, sino en orden alfabético
    # Todavía hay que añadir botones para que se ordene por otras características!
    attendances = reunion.attendances.all().order_by('user__first_name')



    # Utiliza un AJAX request
    if request.method == 'POST':
        asistValue = request.POST.get('asistValue') == 'True' # Transforma el valor del boton en un boolean

        # Cambiar el valor de la instancia de la attendance y guarda los cambios en la base de datos
        attendance = reunion.attendances.get(user = request.user)
        attendance.asistance = asistValue # True si asistValue (que es el value del botton que puede ser Yes o No) es Yes, False si es No (distinto a Yes)
        attendance.save()


    context = {
        'reunion' : reunion,
        'attendances':attendances,
    }

    return render(request, 'reunion.html', context)




# view for the page where you create a reunion by enetering info
def createReunion(request):
    #checks if user is authenticated -> if not -> redirect to login
    if request.user.is_authenticated == False:
        return redirect('/accounts/login')
    
    userForm = UserSelectionFormName()
        

    # APRENDER JQUERY PARA PODER HACER ESTO SIN RECARGAR PAGINA / CAMBIAR URL AL PULSAR BOTONES
    # Alternativamente --> Poner codigo de javascript para que no se borre la informacion en el form al recargar pagina
    if request.method == 'GET':
        searchCriteria = request.GET.get('SearchCriteriaButton')
        print(searchCriteria)

        if searchCriteria == 'Name':
            userForm = UserSelectionFormName

        elif searchCriteria == 'Role':
            userForm = UserSelectionFormRole
        
        elif searchCriteria == 'Class':
            userForm = UserSelectionFormClass
        
    




    if request.method == 'POST' and 'reunionname' in request.POST:

        # Access the input box data

        reunionForm = ReunionForm(request.POST)
        if reunionForm.is_valid():
            input_box_name = reunionForm.cleaned_data['my_name']
            input_box_date = reunionForm.cleaned_data['my_date']
            input_box_description = reunionForm.cleaned_data['my_description']
            Reunion.objects.create(name = input_box_name , date = input_box_date, description = input_box_description)

            # creates reunion first, then adds members 
            # -> thats because to add members i need to create Attendance objects, so its not really an attribute

            # creating Attendance objects, linking Users to the Reunion
            userForm = UserSelectionFormName(request.POST)
            if userForm.is_valid():
                selected_users = userForm.cleaned_data['users']
                for user in selected_users:
                    Attendance.objects.create(user=user, reunion = Reunion.objects.get(name=input_box_name))
            else:
                userForm = UserSelectionFormName()
            
            # redirect to the summary page of the new reunion
            return redirect('../reunion/' + input_box_name)

        else:
            reunionForm = ReunionForm()


    # passing context to the html page for use
    context = {
        'form' : ReunionForm(),
        'userSelectionForm': userForm,
    }
    

    # The render method -> sends info to browser in order to create site
    return render(request, 'createReunion.html', context)  