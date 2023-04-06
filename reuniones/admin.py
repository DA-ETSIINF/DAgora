from django.contrib import admin
from .models import Reunion, Attendance, Document, TempDocument, Role

# Register your models here.


admin.site.register(Reunion)
admin.site.register(Attendance)
admin.site.register(Document)
admin.site.register(TempDocument)

admin.site.register(Role)