from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from registro.models import Registro

def index(request):
    inscritos = Registro.objects.all()
    # print(inscritos)
    return render(request, 'administrador/admin.html', {'inscritos': inscritos}) 
