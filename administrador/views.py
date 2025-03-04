from django.shortcuts import render, redirect
from registro.models import Registro
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import logout


def index(request):
    return render(request, 'administrador/index-inscritos.html') 


def lista_inscritos(request):
    inscritos = Registro.objects.all()
    return render(request, 'administrador/lista-inscritos.html', {'inscritos': inscritos})



def validar_inscrito(request, id):
    
    if request.method == 'POST':
        id = request.POST.get('id', id)  # Usamos el id del formulario si está presente, o el id de la URL por defecto
    
    
    inscrito = Registro.objects.get(id=id)
    inscrito.validado = 0 if inscrito.validado == 1 else 1
    inscrito.save()
    return redirect('lista-inscritos')


def ver_pdf(request):
    context = {'pdf_url': '/media/pdfs/'}
    return render(request, 'show_pdf.html', context)


# CRAER Y LOGIN DEL ADMINISTRADOR

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Autenticar al usuario
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index-inscritos')  # Redirige a la página de inicio
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
        else:
            messages.error(request, 'Por favor, corrige los errores.')
    else:
        form = AuthenticationForm()

    return render(request, 'administrador/login-administrador.html', {'form': form})


def logout_view(request):
    logout(request)  # Cierra la sesión del usuario
    return redirect('login')  # Redirige a la página de login o cualquier otra página pública


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda el nuevo usuario
            messages.success(request, '¡Cuenta creada exitosamente! Ahora puedes iniciar sesión.')
            return redirect('index-inscritos')  # Redirige al login después de crear la cuenta
        else:
            messages.error(request, 'Por favor, corrige los errores.')
    else:
        form = UserCreationForm()

    return render(request, 'administrador/crear-administrador.html', {'form': form})