from django.shortcuts import render, redirect
from django.db import IntegrityError
from .forms import RegistroForm
from django.http import JsonResponse
from .models import Registro  # Importa tu modelo, si lo tienes


def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST, request.FILES)  # Subir archivos (pdf) con request.FILES
        if form.is_valid():
            print('Formulario válido:', form.cleaned_data)
            
            try:
                form.save()
                print('Registro guardado con éxito')
                return redirect('landing_page')  # Redirige a la página de inicio o a donde sea
            except IntegrityError as e:
                # Aquí manejamos la excepción de violación de unicidad
                if 'dni' in str(e):
                    form.add_error('dni', 'El DNI ya existe. Por favor, ingrese un DNI único.')
                elif 'email' in str(e):
                    form.add_error('email', 'El correo electrónico ya está registrado.')
                elif 'celular' in str(e):
                    form.add_error('celular', 'El número de celular ya está registrado.')

                print('Error al guardar el registro:', e)
        else:
            print('Errores del formulario:', form.errors)
    else:
        form = RegistroForm()

    return render(request, 'registro/registro.html', {'form': form})


def validar_duplicados(request):
    # Obtener los parámetros enviados desde el frontend
    
    dni = request.GET.get('dni')
    email = request.GET.get('email')
    celular = request.GET.get('celular')
    
    # Crear un diccionario para los errores
    response_data = {}

    # Validar si el DNI ya está registrado
    if Registro.objects.filter(dni=dni).exists():  # Ajusta esto según tu modelo
        response_data['dni'] = 'El DNI ya está registrado.'

    # Validar si el correo electrónico ya está registrado
    if Registro.objects.filter(email=email).exists():  # Ajusta esto según tu modelo
        response_data['email'] = 'El correo electrónico ya está registrado.'

    # Validar si el celular ya está registrado
    if Registro.objects.filter(celular=celular).exists():  # Ajusta esto según tu modelo
        response_data['celular'] = 'El número de celular ya está registrado.'

    # Si existen duplicados, devolver los errores
    if response_data:
        return JsonResponse(response_data)
    else:
        return JsonResponse({'success': True})  # Si no hay duplicados, devolver éxito