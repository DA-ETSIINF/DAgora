from django.shortcuts import render, redirect
from custom_profiles.models import Role, Group, Permission
from reunion_system.models import Meeting, Attendance, File
from django.contrib.auth.models import User
from django.conf import settings
from django.http import JsonResponse
from django.db.models import Q
from django.utils import timezone
from django.core.files.storage import default_storage


def homePage(request):
    # checks if user is authenticated -> if not -> asks for login
    if request.user.is_authenticated == False:
        return redirect('/accounts/login')
    
    user = request.user
    meeting_list = Meeting.objects.all().order_by('date', 'time')
    now = timezone.localtime(timezone.now()) # So it doesnt happen that timezone.now() is different 
    future_meetings = Meeting.objects.filter(
        Q(date__gt=now.date()) | (Q(date=now.date()) & Q(time__gte=now.time()))
    ).order_by('date', 'time')

    past_meetings = Meeting.objects.filter(
        Q(date__lt=now.date()) | (Q(date=now.date()) & Q(time__lt=now.time()))
    ).order_by('-date', '-time')

    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        user.userprofile.show_email = request.POST['show_email']=="true"
        user.userprofile.save()


    context = {
        'user' : user,
        'meeting_list' : meeting_list,
        'future_meetings' : future_meetings,
        'past_meetings' : past_meetings,
        }

    return render(request, 'home.html', context)

# Overview page for meetings
def meetingInfo(request, meeting_id):
    # checks if user is authenticated -> if not -> asks for login
    if request.user.is_authenticated == False:
        return redirect('/accounts/login')
    
    
    meeting = Meeting.objects.get(id = meeting_id)
    # check if user is supposed to have acces to the meeting -> if not -> redirect to home
    if not Attendance.objects.filter(user = request.user, meeting = meeting):
        return redirect('../../')
    
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
    
    #checks if user can create a meeting -> if not -> redirect to home
    if not request.user.userprofile.can_create_meeting():
        return redirect('../')
    

    if request.method == 'POST'and request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.POST['post_type'] == 'meeting_submit':
        
        meeting_name = request.POST['meeting_name']
        meeting_date = request.POST['meeting_date']
        meeting_time = request.POST['meeting_time']
        meeting_description = request.POST['meeting_description']

        new_meeting = Meeting.objects.create(name=meeting_name, date=meeting_date, time = meeting_time, description=meeting_description, creator = request.user)

        # create attendance instances for selected users
        if request.POST['submited_users_Ids'] != '': # If there have been Ids submitted
            user_ids = request.POST['submited_users_Ids'].split(' ')
            for id in user_ids:
                #check if user can be called by creator -> By changing ids in the html document other users than intended can be added to the meeting
                user = User.objects.get(id=id)
                if request.user.userprofile.can_call_user(user):
                    Attendance.objects.create(user = user, meeting = new_meeting) 


        # create attendance instance for user/creator (so people dont accidentaly not add themselves to their meeting)
        if not Attendance.objects.filter(user=request.user, meeting=new_meeting):
            Attendance.objects.create(user = request.user, meeting = new_meeting)


        # handle files
        files = request.FILES.getlist('files')

        for file in files:
            File.objects.create(meeting=new_meeting,file=file)

        
        return JsonResponse({'redirect':True,'meeting_id':new_meeting.id})        

    
    context = {
        'callable_groups': request.user.userprofile.callable_groups(),
        'groups':Group.objects.all(),
    }

    return render(request, 'create_meeting.html', context) 

def meeting_edit(request, meeting_id):
    #checks if user is authenticated -> if not -> redirect to login
    if request.user.is_authenticated == False:
        return redirect('/accounts/login')
    
    meeting = Meeting.objects.get(id = meeting_id)
    #checks if user has perms to edit meeting -> if not -> redirect to info page 
    if meeting.creator != request.user:
        return redirect('./')
    

    if request.method == 'POST'and request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.POST['post_type'] == 'meeting_submit':

        meeting.name = request.POST['meeting_name']
        meeting.date = request.POST['meeting_date']
        meeting.description = request.POST['meeting_description']
        meeting.save()

        # handle file deletion
        file_ids = request.POST.getlist('file_id')
        for id in file_ids:
            #check if the file is part of the meeting -> so people dont delete other files by changing ids in the html of the site
            file = File.objects.get(id = id)
            if file.meeting == meeting:
                File.objects.get(id = id).delete()

        # handle files
        files = request.FILES.getlist('files')

        for file in files:
            File.objects.create(meeting=meeting,file=file)


        return JsonResponse({'redirect':True}) #Javascript has to handle redirect
        

    context = {
        'meeting' : meeting,
        'files':File.objects.filter(meeting=meeting),
    }
    return render(request,'meeting_edit.html', context)

def userlist(request):
    #checks if user is authenticated -> if not -> redirect to login
    if request.user.is_authenticated == False:
        return redirect('/accounts/login')
    
    
    
    context = {
        'users' : User.objects.all(),
    }
    
    return render(request, 'userlist.html', context)

def profile(request):
    #checks if user is authenticated -> if not -> redirect to login
    if request.user.is_authenticated == False:
        return redirect('/accounts/login')
    
    context = {
        'meetings' : Meeting.objects.all(),
        'profile' : request.user,

    }
    
    return render(request, 'profile.html', context)

#Auxiliary functions:

        


    
