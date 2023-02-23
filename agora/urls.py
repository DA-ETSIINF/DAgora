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
from django.views.generic.base import TemplateView
from custom_profiles import views
from reuniones.views import reunionAsistances, createReunion, main, file_upload

# for file view during developement
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', main, name='home'),
    path('reunion/<str:reunion_name>/', reunionAsistances, name = 'reunionAsistances'),
    path('createReunion/', createReunion, name = 'createReunion'),

    # Testviews for file uploading
    # Add one <dir>/upload/ path for every dir that uses the upload system!
    path('upload/', file_upload),
    path('createReunion/upload/', file_upload),
]

# Enables the viewing of uploaded documents by introducing the url --> only for developement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)