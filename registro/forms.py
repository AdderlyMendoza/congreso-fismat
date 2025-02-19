from django import forms
from .models import Registro

class RegistroForm(forms.ModelForm):
    class Meta:
        model = Registro
        fields = ['dni', 'nombres', 'apellido_paterno' , 'apellido_materno', 'email', 'telefono']        
        widgets = {
            'dni': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'DNI'}),            
            'nombres': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombres'}),
            'apellido_paterno': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido Paterno'}),
            'apellido_materno': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido Materno'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Tu Email'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu Teléfono'}),
        }
