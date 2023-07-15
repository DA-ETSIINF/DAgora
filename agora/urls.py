"""agora URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from reunion_system.views import homePage, meetingInfo, create_meeting, meeting_edit


# for file view during developement
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),

    path('', homePage, name = 'home'), # name so we can make buttons with {% url = 'home' %}
    path('create_new_meeting/', create_meeting, name = 'create_new_meeting'),
    path('meeting/<str:meeting_name>/', meetingInfo, name = 'meeting_info'),
    path('meeting/<str:meeting_name>/edit', meeting_edit, name = 'meeting_edit'),

]

# Enables the viewing of uploaded documents by introducing the url --> only for developement
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
