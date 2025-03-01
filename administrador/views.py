from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from registro.models import Registro

def index(request):
    return render(request, 'administrador/index-inscritos.html') 


def lista_inscritos(request):
    inscritos = Registro.objects.all()
    return render(request, 'administrador/lista-inscritos.html', {'inscritos': inscritos})


def ver_pdf(request):
    context = {'pdf_url': '/media/pdfs/'}
    return render(request, 'show_pdf.html', context)