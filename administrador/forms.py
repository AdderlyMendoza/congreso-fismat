# forms.py
from django import forms

class EntradaForm(forms.Form):
    dni = forms.CharField(max_length=8, required=True, label="DNI")
    ubicacion = forms.ChoiceField(choices=[('A', 'Lugar A'), ('B', 'Lugar B'), ('C', 'Lugar C'), ('D', 'Lugar D')])


class SalidaForm(forms.Form):
    dni = forms.CharField(max_length=8, required=True, label="DNI")
    ubicacion = forms.ChoiceField(choices=[('A', 'Lugar A'), ('B', 'Lugar B'), ('C', 'Lugar C'), ('D', 'Lugar D')])




# roles y permisos
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group


class CustomUserCreationForm(UserCreationForm):
    role_choices = (
        ('administrador', 'Administrador'),
        ('asistencia', 'Asistencia'),
    )
    role = forms.ChoiceField(
        choices=role_choices,
        label='Rol',
        widget=forms.RadioSelect(attrs={'class': 'form-radio text-lg text-gray-700'})
    )

    username = forms.CharField(
        max_length=100,
        required=True,
        label="Usuario",
        widget=forms.TextInput(attrs={
            'class': 'form-input p-2 border-2 border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 w-full',
            'placeholder': 'Nombre de usuario'
        })
    )

    password1 = forms.CharField(
        max_length=100,
        required=True,
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-input p-2 border-2 border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 w-full',
            'placeholder': 'Contraseña'
        })
    )

    password2 = forms.CharField(
        max_length=100,
        required=True,
        label="Confirmar Contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-input p-2 border-2 border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 w-full',
            'placeholder': 'Confirma tu contraseña'
        })
    )

    phone = forms.CharField(
        max_length=15,
        required=True,
        label="Teléfono",
        widget=forms.TextInput(attrs={
            'class': 'form-input p-2 border-2 border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 w-full',
            'placeholder': 'Número de teléfono'
        })
    )

    first_name = forms.CharField(
        max_length=100,
        required=True,
        label="Nombre Completo",
        widget=forms.TextInput(attrs={
            'class': 'form-input p-2 border-2 border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 w-full',
            'placeholder': 'Nombre completo'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'phone', 'role']
