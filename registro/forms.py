from django import forms
from .models import Registro

class RegistroForm(forms.ModelForm):
    class Meta:
        model = Registro
        fields = ['dni', 'nombres', 'apellido_paterno' , 'apellido_materno', 'email', 'celular', 'proyecto_investigacion']        
        widgets = {
            'dni': forms.TextInput(attrs={'class': 'form-control mt-1 w-full border p-3 rounded-md focus:outline-none focus:border-2 focus:border-blue-500', 'placeholder': 'DNI'}),            
            'nombres': forms.TextInput(attrs={'class': 'form-control mt-1 w-full border p-3 rounded-md focus:outline-none focus:border-2 focus:border-blue-500', 'placeholder': 'Nombres'}),
            'apellido_paterno': forms.TextInput(attrs={'class': 'form-control mt-1 w-full border p-3 rounded-md focus:outline-none focus:border-2 focus:border-blue-500', 'placeholder': 'Apellido Paterno'}),
            'apellido_materno': forms.TextInput(attrs={'class': 'form-control mt-1 w-full border p-3 rounded-md focus:outline-none focus:border-2 focus:border-blue-500', 'placeholder': 'Apellido Materno'}),
            'email': forms.EmailInput(attrs={'class': 'form-control mt-1 w-full border p-3 rounded-md focus:outline-none focus:border-2 focus:border-blue-500', 'placeholder': 'Email'}),
            'celular': forms.TextInput(attrs={'class': 'form-control mt-1 w-full border p-3 rounded-md focus:outline-none focus:border-2 focus:border-blue-500', 'placeholder': 'Número de celular'}),
            'proyecto_investigacion': forms.FileInput(attrs={'class': 'form-control w-full pl-15 bg-gray-100 border-2 border-gray-300 py-2 px-4 mt-1 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-300 ease-in-out hover:border-blue-400 focus:outline-none'}),
        }
