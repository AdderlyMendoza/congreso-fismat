from django.shortcuts import render, redirect
from registro.models import Registro
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import logout
from .models import Asistencia
from django.utils import timezone

from .forms import EntradaForm, SalidaForm


from datetime import timedelta




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



def entrada_inscritos(request):
    if request.method == 'POST':
        form = EntradaForm(request.POST)
        if form.is_valid():
            dni = form.cleaned_data['dni']
            try:
                # Buscar al usuario con el DNI proporcionado
                usuario = Registro.objects.get(dni=dni)

                # Verificar si ya existe un registro de asistencia para este usuario y la fecha actual
                asistencia = Asistencia.objects.filter(usuario=usuario, fecha=timezone.now().date()).first()
                print("registro de entrada: ", timezone.localtime(timezone.now()))

                if not asistencia:
                    # Si no existe el registro, creamos uno nuevo con la hora de entrada
                    hora_ajustada = timezone.localtime(timezone.now()) - timedelta(hours=5)
                    
                    asistencia = Asistencia.objects.create(
                        usuario=usuario,
                        entrada=hora_ajustada,
                        fecha=timezone.now().date()
                    )
                    form.add_error('dni', 'El usuario registrado.')
                    
                else:
                    # Si ya existe el registro, no hacemos nada
                    form.add_error('dni', 'El usuario con este DNI ya está registrado.')
                    
                    pass

                return redirect('entrada-inscritos')  # Redirige después de registrar
            except Registro.DoesNotExist:
                form.add_error('dni', 'El usuario con este DNI no existe.')
    else:
        form = EntradaForm()

    return render(request, 'administrador/entrada-inscritos.html', {'form': form})



def salida_inscritos(request):
    if request.method == 'POST':
        form = SalidaForm(request.POST)
        if form.is_valid():
            dni = form.cleaned_data['dni']
            try:
                # Buscar al usuario con el DNI proporcionado
                usuario = Registro.objects.get(dni=dni)

                ## LA ENTRADA TIENE QUE ALMACENARSE CON HORA Y LA SALIDA TAMBIEN, LA COLUMNA FECHA QUE SIGA SIENDO SOLO AÑO/MES/DIA
                asistencia = Asistencia.objects.filter(usuario=usuario, fecha=timezone.localtime(timezone.now()).date()).first()
                print("registro de salida: ", timezone.localtime(timezone.now()))
                

                if asistencia:
                    if asistencia.entrada is not None and asistencia.salida is None:
                        # Si ya existe un registro de entrada y no tiene salida, actualizamos la salida
                        hora_ajustada = timezone.localtime(timezone.now()) - timedelta(hours=5)
                        asistencia.salida = hora_ajustada
                        asistencia.save()
                    else:
                        # Si no tiene entrada o ya tiene salida, mostramos un error
                        form.add_error('dni', 'No se puede registrar una salida sin una entrada, o ya se registró una salida.')
                else:
                    # Si no existe el registro de asistencia, mostramos un error
                    form.add_error('dni', 'No existe un registro de entrada para este usuario hoy.')

                return redirect('salida-inscritos')  # Redirige después de registrar
            
            except Registro.DoesNotExist:
                form.add_error('dni', 'El usuario con este DNI no existe.')
    else:
        form = SalidaForm()

    return render(request, 'administrador/salida-inscritos.html', {'form': form})





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
            messages.error(request, 'Usuario y/o contraseña incorrectos.')
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
            return redirect('login')  # Redirige al login después de crear la cuenta
        else:
            messages.error(request, 'Por favor, corrige los errores.')
    else:
        form = UserCreationForm()

    return render(request, 'administrador/crear-administrador.html', {'form': form})