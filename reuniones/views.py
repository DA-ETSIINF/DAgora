from django.shortcuts import render, redirect
from .models import Reunion, Attendance, Document, TempDocument
from custom_profiles.models import UserProfile
from .forms import ReunionForm, UserSelectionFormName, FileUploadForm
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from django.http import JsonResponse #JQuery AJAX requests
from pathlib import Path
from django.core.files import File
import os
import shutil


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
    documents = Document.objects.filter(reunions = reunion)
    editPerms = reunion.creator == request.user


    # el order.by es para que no se coloquen en orden de creación, sino en orden alfabético
    # Todavía hay que añadir botones para que se ordene por otras características!
    attendances = reunion.attendances.all().order_by('user__first_name')



    # Utiliza un AJAX request
    # el and request.headers.get('x-requested-with') == 'XMLHttpRequest' mira si la request es ajax o no -> Para evitar errores
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        asistValue = request.POST.get('asistValue') == 'True' # Transforma el valor del boton en un boolean

        # Cambiar el valor de la instancia de la attendance y guarda los cambios en la base de datos
        attendance = reunion.attendances.get(user = request.user)
        attendance.asistance = asistValue # True si asistValue (que es el value del botton que puede ser Yes o No) es Yes, False si es No (distinto a Yes)
        attendance.save()




    context = {
        'reunion' : reunion,
        'attendances':attendances,
        'documents':documents,
        'editPerms':editPerms,
    }


    return render(request, 'reunion.html', context)

def reunionEdit(request, reunion_name):
    reunion = Reunion.objects.get(name = reunion_name)
    documents = Document.objects.filter(reunions = reunion)
    # reunionForm is pre-filled with old info so its easier to edit
    reunionForm = ReunionForm(initial={'my_name':reunion.name, 'my_date':reunion.date, 'my_description':reunion.description})

    if request.method == 'GET':
        #reset session so it can be used again without re-adding the same documents
        request.session['documents'] = []

    
    # Submit ReunionForm with new values -> edition of basic Info
    if request.method == 'POST' and 'submitButton' in request.POST:
        reunionForm = ReunionForm(request.POST)
        if reunionForm.is_valid():

            reunion.name = reunionForm.cleaned_data['my_name']
            reunion.date = reunionForm.cleaned_data['my_date']
            reunion.description = reunionForm.cleaned_data['my_description']
            reunion.save()


            return redirect ('../../' + reunion.name + '/edit') 
    
    # Delete document buttons -> Uses AJAX
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.POST['post_type'] == 'file_deletion':
        docName = request.POST['documentName'].strip()
        document = Document.objects.filter(title = docName)
        document.delete()
        print(docName)

    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.POST['post_type'] == 'file_submit':
        for document_id in request.session['documents']:
            
            # Get tempDocument with the file we want to add to the reunion
            tempDocu = TempDocument.objects.get(id = document_id)
            
            # Duplicate the file of the tempDoc to media/documents (instead of temp)
            # We need two separate files in order for there to not be any problems between the tempDocument and Document models

            initial_path = tempDocu.file.path
            file_name="documents/" + tempDocu.file.name[len("temp/documents/"):]
            new_path = os.path.join(settings.MEDIA_ROOT,file_name)
            shutil.copy(initial_path, new_path)
            
            # Open duplicated file in media/documents/ and create a new Document instance with the file linked to it
            with open(initial_path, 'rb') as f:
                file_obj = File(f)

                new_document = Document()

                new_document.title = tempDocu.title # Same title as the old document
                new_document.file.save(os.path.basename(new_path), file_obj)
                os.remove(new_path)
                
            # Add document to the reunion instance
            reunion.documents.add(new_document)

        print('simonsais')

    context = {
        'reunion':reunion,
        'documents':documents,
        'reunionForm':reunionForm,
    }
    return render(request, 'reunionEdition.html', context)




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



        

    if request.method == 'POST' and 'reunionname' in request.POST:
        

        # Access the input box data

        reunionForm = ReunionForm(request.POST)
        if reunionForm.is_valid():
            input_box_name = reunionForm.cleaned_data['my_name']
            input_box_date = reunionForm.cleaned_data['my_date']
            input_box_description = reunionForm.cleaned_data['my_description']
            Reunion.objects.create(name = input_box_name , date = input_box_date, description = input_box_description, creator=request.user)

            # creates reunion first, then adds members 
            # -> thats because to add members i need to create Attendance objects, so its not really an attribute

            # creating Attendance objects, linking Users to the Reunion
            userForm = UserSelectionFormName(request.POST)
            if userForm.is_valid():
                selected_users = userForm.cleaned_data['users']
                for user in selected_users:
                    Attendance.objects.create(user=user, reunion = Reunion.objects.get(name=input_box_name))
                # Puts the reunion creator in the reunion if he didnt select himself
                if not Attendance.objects.filter(user = request.user, reunion = Reunion.objects.get(name=input_box_name)):
                    Attendance.objects.create(user=request.user, reunion = Reunion.objects.get(name=input_box_name))
            else:
                userForm = UserSelectionFormName()
            

            for document_id in request.session['documents']:

                # Get tempDocument with the file we want to add to the reunion
                tempDocu = TempDocument.objects.get(id = document_id)
                
                # Duplicate the file of the tempDoc to media/documents (instead of temp)
                # We need two separate files in order for there to not be any problems between the tempDocument and Document models

                initial_path = tempDocu.file.path

                file_name="documents/" + tempDocu.file.name[len("temp/documents/"):]
                
                new_path = os.path.join(settings.MEDIA_ROOT,file_name)

                shutil.copy(initial_path, new_path)
                
                # Open duplicated file in media/documents/ and create a new Document instance with the file linked to it
                with open(initial_path, 'rb') as f:
                    file_obj = File(f)

                    new_document = Document()

                    new_document.title = tempDocu.title # Same title as the old document
                    new_document.file.save(os.path.basename(new_path), file_obj)
                    os.remove(new_path)
                    



                # Add document to the reunion instance
                Reunion.objects.get(name=input_box_name).documents.add(new_document)
            
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



# Create Document instances with files uploaded via Dropzone box
def file_upload(request):
    if request.method == 'POST':
        my_file=request.FILES.get('file')
        document = TempDocument.objects.create(title=my_file.name, file=my_file, creation_date = timezone.now())
        # Save ID to session so it can then be used in the corresponding view
        request.session.setdefault('documents',[]).append(document.id)
        request.session.save()
    return JsonResponse({'post':'fasle'})

def edition_file_upload(request, reunion_name):
    if request.method == 'POST':
        my_file=request.FILES.get('file')
        document = TempDocument.objects.create(title=my_file.name, file=my_file, creation_date = timezone.now())
        # Save ID to session so it can then be used in the corresponding view
        request.session.setdefault('documents',[]).append(document.id)
        request.session.save()
    return JsonResponse({'post':'fasle'})