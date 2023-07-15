from django.contrib import admin

from reunion_system.models import Meeting, Attendance, File

# Register your models here.


class FileInline(admin.TabularInline):
    model = File
    extra = 1

class AttendanceInline(admin.TabularInline):
    model = Attendance
    extra = 1

@admin.register(Meeting)  #Registers Meeting but adding a tab for its files and users
class MeetingAdmin(admin.ModelAdmin):
    inlines = [FileInline, AttendanceInline]