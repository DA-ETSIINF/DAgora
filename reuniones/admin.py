from django.contrib import admin
from .models import Reunion, Attendance, Document

# Register your models here.


admin.site.register(Reunion)
admin.site.register(Attendance)
admin.site.register(Document)