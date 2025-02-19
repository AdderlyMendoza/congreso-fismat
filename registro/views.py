from django.shortcuts import render, redirect
from .forms import RegistroForm

def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inscripcion_exitosa')  # Redirigir a una página de éxito
    else:
        form = RegistroForm()
    
    return render(request, 'registro/registro.html', {'form': form})
