# forms.py
from django import forms

class EntradaForm(forms.Form):
    dni = forms.CharField(max_length=8, required=True, label="DNI")

class SalidaForm(forms.Form):
    dni = forms.CharField(max_length=8, required=True, label="DNI")
