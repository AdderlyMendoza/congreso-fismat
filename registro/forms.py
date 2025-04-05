from django import forms
from .models import Registro

# ESTUDIANTE = 'estudiante (solo pregrado)'
# PARTICIPANTE = 'participante'
    
# TIPO_PARTICIPANTE_CHOICES = [
#     ('', 'Seleccione'),
#     (ESTUDIANTE, 'Estudiante (solo pregrado)'),
#     (PARTICIPANTE, 'Participante'),
# ]


class RegistroForm(forms.ModelForm):
    
    class Meta:
        model = Registro
        fields = ['pais', 'entidad_procedencia', 'tipo_participante', 'doc_acreditivo', 'dni', 'nombres', 'apellido_paterno' , 'apellido_materno', 'email', 'celular', 'voucher_pago']        
        widgets = {
            'pais': forms.Select(attrs={'class': 'form-control mt-1 w-full border p-3 rounded-md focus:outline-none focus:border-2 focus:border-blue-500', 'placeholder': 'País', 'required': True}),
            'entidad_procedencia': forms.TextInput(attrs={'class': 'form-control mt-1 w-full border p-3 rounded-md focus:outline-none focus:border-2 focus:border-blue-500', 'placeholder': 'Entidad de Procedencia', 'required': True}),
            'tipo_participante': forms.Select(attrs={'class': 'form-control mt-1 w-full border p-3 rounded-md focus:outline-none focus:border-2 focus:border-blue-500', 'placeholder': 'Tipo de Participante', 'required': True}),
            
            'doc_acreditivo': forms.FileInput(attrs={'class': 'form-control w-full p-3 bg-gray-100 border-2 border-gray-300 py-2 px-4 mt-1 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-300 ease-in-out hover:border-blue-400 focus:outline-none'}),
            
            'dni': forms.TextInput(attrs={'class': 'form-control mt-1 w-full border p-3 rounded-md focus:outline-none focus:border-2 focus:border-blue-500', 'placeholder': 'DNI', 'required': True}),            
            'nombres': forms.TextInput(attrs={'class': 'form-control mt-1 w-full border p-3 rounded-md focus:outline-none focus:border-2 focus:border-blue-500', 'placeholder': 'Nombres', 'required': True}),
            'apellido_paterno': forms.TextInput(attrs={'class': 'form-control mt-1 w-full border p-3 rounded-md focus:outline-none focus:border-2 focus:border-blue-500', 'placeholder': 'Apellido Paterno', 'required': True}),
            'apellido_materno': forms.TextInput(attrs={'class': 'form-control mt-1 w-full border p-3 rounded-md focus:outline-none focus:border-2 focus:border-blue-500', 'placeholder': 'Apellido Materno', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control mt-1 w-full border p-3 rounded-md focus:outline-none focus:border-2 focus:border-blue-500', 'placeholder': 'Email', 'required': True}),
            'celular': forms.TextInput(attrs={'class': 'form-control mt-1 w-full border p-3 rounded-md focus:outline-none focus:border-2 focus:border-blue-500', 'placeholder': 'Número de celular', 'required': True}),
            
            'voucher_pago': forms.FileInput(attrs={'class': 'form-control w-full p-3 bg-gray-100 border-2 border-gray-300 py-2 px-4 mt-1 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-300 ease-in-out hover:border-blue-400 focus:outline-none', 'required': True}),
        }
        
    def clean(self):
        cleaned_data = super().clean()
        tipo_participante = cleaned_data.get('tipo_participante')
        doc_acreditivo = cleaned_data.get('doc_acreditivo')

        if tipo_participante == 'estudiante' and not doc_acreditivo:
            self.add_error('doc_acreditivo', 'El documento acreditivo es obligatorio para los estudiantes.')
        
        return cleaned_data