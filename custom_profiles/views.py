from django.shortcuts import render, redirect
from reuniones.models import Reunion
from django.contrib.auth.models import User



# Create your views here.

# MOVER LUEGO A REUNIONES! ESTA APP ES SOLO PARA LOGIN Y LA EXTENSION DE ATRIBUTOS DE LOS USUARIOS
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

