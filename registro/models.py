from django.db import models
from django_countries.fields import CountryField

import mimetypes
from django.core.exceptions import ValidationError


SELECCIONE = 'Seleccione'
ESTUDIANTE = 'estudiante (pregrado)'
PARTICIPANTE = 'participante'

TIPO_PARTICIPANTE_CHOICES = [
    ('', '(Seleccione)'),
    (ESTUDIANTE, 'Estudiante (pregrado)'),
    (PARTICIPANTE, 'Participante'),
]

class Registro(models.Model):
    pais = CountryField(blank_label='(Seleccione el país)')
    entidad_procedencia = models.CharField(max_length=100, blank=False, null=False)  # Entidad de procedencia
    tipo_participante = models.CharField(
        max_length=50, 
        choices=TIPO_PARTICIPANTE_CHOICES, 
        default=SELECCIONE,
        blank=False, 
        null=False
    )

    doc_acreditivo = models.FileField(max_length=100, blank=True, null=True)  # Documento si es estudiante
    
    monto = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False, default=0.00)
    
    dni = models.CharField(max_length=15, blank=False, null=False, unique=True) # o carnet de extranjeria
    nombres = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    email = models.EmailField(unique=True)  # Correo electrónico único
    celular = models.CharField(max_length=15, blank=True, null=False, unique=True)  # Celular único

    voucher_pago = models.FileField(upload_to='pdfs/', blank=True, null=False)  # Hacerlo opcional prueba para PRODUCCION

    validado = models.BooleanField(default=False)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"id: {self.id}, Entidad de Procedencia: {self.entidad_procedencia}, Tipo de Participante: {self. tipo_participante}, Documento de Estudiante {self.doc_acreditivo} DNI: {self.dni}, Nombres: {self.nombres}, Apellido Paterno: {self.apellido_paterno}, " f"Apellido Materno: {self.apellido_materno}, Email: {self.email}, Celular: {self.celular}, " f"Voucher de Pago: {self.voucher_pago}, Fecha de Registro: {self.fecha_registro}, Validado: {self.validado}"
