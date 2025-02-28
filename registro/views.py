from django.shortcuts import render, redirect
from .forms import RegistroForm

def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST, request.FILES) # subir archivos (pdf) con request.FILES
        if form.is_valid():
            print('Formulario válido:', form.cleaned_data)
            
            try:
                form.save()
                print('Registro guardado con éxito')
            except Exception as e:
                print('Error al guardar el registro:', e)

            return redirect('landing_page') # Redirige a la pagWeb
        else:
            print('Errores del formulario:', form.errors)
    else:
        form = RegistroForm()

    return render(request, 'registro/registro.html', {'form': form})
