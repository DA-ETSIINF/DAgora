from django.shortcuts import render, redirect
from .models import Reunion, Attendance, Document, TempDocument
from custom_profiles.models import UserProfile
from .forms import ReunionForm, UserSelectionFormName, FileUploadForm
from django.contrib.auth.models import User
from django.utils import timezone
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
    #fileForm = FileUploadForm()  -> Replaced by Dropzone
        

    if request.method == 'GET':

        #reset session so it can be used again without re-adding the same documents
        request.session['documents'] = []



    if request.method == 'POST':
        print(request.POST.get('usedForm'))
        

    if request.method == 'POST' and 'reunionname' in request.POST:
        print(request.POST.get('usedForm'))
        

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
            

            # add documents to the reunion documents attribute
            for document_id in request.session['documents']:
                tempDocu = TempDocument.objects.get(id = document_id)
                document = Document.objects.create(title = tempDocu.title, file = tempDocu.file)
                Reunion.objects.get(name=input_box_name).documents.add(document)
            
            # redirect to the summary page of the new reunion
            #return redirect('../reunion/' + input_box_name)

        else:
            reunionForm = ReunionForm()


    # passing context to the html page for use
    context = {
        'form' : ReunionForm(),
        'userSelectionForm': userForm,
    }
    

    # The render method -> sends info to browser in order to create site
    return render(request, 'createReunion.html', context)  



# Create Document instances with files uploaded via Dropzone box
def file_upload(request):
    if request.method == 'POST':
        my_file=request.FILES.get('file')
        document = TempDocument.objects.create(title=my_file.name, file=my_file, creation_date = timezone.now())
        # Save ID to session so it can then be used in the corresponding view
        request.session.setdefault('documents',[]).append(document.id)
        request.session.save()
        print(request.session['documents'])
    return JsonResponse({'post':'fasle'})