from django.shortcuts import render, redirect
from custom_profiles.models import Role, Group, Permission
from reunion_system.models import Meeting, Attendance, File
from django.contrib.auth.models import User
from django.conf import settings
from django.http import JsonResponse
from django.core.files.storage import default_storage


def homePage(request):
    # checks if user is authenticated -> if not -> asks for login
    if request.user.is_authenticated == False:
        return redirect('/accounts/login')
    
    user = request.user
    meeting_list = Meeting.objects.all()

    context = {
        'user' : user,
        'meeting_list' : meeting_list,
        }

    return render(request, 'home.html', context)

# Overview page for meetings
def meetingInfo(request, meeting_name):
    # checks if user is authenticated -> if not -> asks for login
    if request.user.is_authenticated == False:
        return redirect('/accounts/login')
    
    meeting = Meeting.objects.get(name = meeting_name)
    files = File.objects.filter(meeting=meeting)
    editPerms = meeting.creator == request.user

    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        attendance_value = request.POST.get('attendance') == 'true'

        attendance_instance = meeting.attendances.get(user = request.user)
        attendance_instance.attendance = attendance_value
        attendance_instance.save()

    context = {
        'meeting' : meeting,
        'files':files,
        'editPerms':editPerms,
        'roles': Role.objects.all(),
        'groups': Group.objects.all(),
    }

    return render(request, 'meeting_info.html', context)

# Page were you create a new meeting
def create_meeting(request):
    #checks if user is authenticated -> if not -> redirect to login
    if request.user.is_authenticated == False:
        return redirect('/accounts/login')
    

    if request.method == 'POST'and request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.POST['post_type'] == 'meeting_submit':
        #check if name is already in use
        if Meeting.objects.filter(name=request.POST['meeting_name']):
            return JsonResponse({'redirect':False})
        
        meeting_name = request.POST['meeting_name']
        meeting_date = request.POST['meeting_date']
        meeting_description = request.POST['meeting_description']

        Meeting.objects.create(name=meeting_name, date=meeting_date, description=meeting_description, creator = request.user)

        # create attendance instances for selected users
        if request.POST['submited_users_Ids'] != '': # If there have been Ids submitted
            user_ids = request.POST['submited_users_Ids'].split(' ')
            for id in user_ids:
                Attendance.objects.create(user = User.objects.get(id=id), meeting = Meeting.objects.get(name=meeting_name))

        #still have to check if the user is someone that can be called to the meeting (to prevent exploits)!




        # create attendance instance for user/creator (so people dont accidentaly not add themselves to their meeting)
        if not Attendance.objects.filter(user=request.user, meeting=Meeting.objects.get(name=meeting_name)):
            Attendance.objects.create(user = request.user, meeting = Meeting.objects.get(name=meeting_name))


        # handle files
        files = request.FILES.getlist('files')

        for file in files:
            File.objects.create(meeting=Meeting.objects.get(name=meeting_name),file=file)

        
        return JsonResponse({'redirect':True})        

    
    context = {
        'callable_roles': request.user.userprofile.callable_roles(),
    }

    return render(request, 'create_meeting.html', context) 

def meeting_edit(request, meeting_name):
    meeting = Meeting.objects.get(name = meeting_name)
    files = File.objects.filter(meeting=meeting)

    if request.method == 'POST'and request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.POST['post_type'] == 'meeting_submit':

        meeting.name = request.POST['meeting_name']
        meeting.date = request.POST['meeting_date']
        meeting.description = request.POST['meeting_description']
        meeting.save()

        # handle file deletion
        file_ids = request.POST.getlist('file_id')
        for id in file_ids:
            File.objects.get(id = id).delete()


        # handle files
        files = request.FILES.getlist('files')

        for file in files:
            File.objects.create(meeting=Meeting.objects.get(name=meeting_name),file=file)


        return JsonResponse({'redirect':True})
        

    context = {
        'meeting' : meeting,
        'files':files,
    }
    return render(request,'meeting_edit.html', context)



#Auxiliary functions:

        


    
