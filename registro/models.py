from django.db import models

class Registro(models.Model):
    dni = models.CharField(max_length=8, blank=False, null=False, unique=True)  # DNI único
    nombres = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    email = models.EmailField(unique=True)  # Correo electrónico único
    celular = models.CharField(max_length=15, blank=True, null=False, unique=True)  # Celular único
    proyecto_investigacion = models.FileField(upload_to='pdfs/', blank=True, null=True)  # Hacerlo opcional prueba para PRODUCCION
    validado = models.BooleanField(default=False)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"id: {self.id}, DNI: {self.dni}, Nombres: {self.nombres}, Apellido Paterno: {self.apellido_paterno}, " \
               f"Apellido Materno: {self.apellido_materno}, Email: {self.email}, Celular: {self.celular}, " \
               f"Proyecto: {self.proyecto_investigacion}, Fecha de Registro: {self.fecha_registro}, Validado: {self.validado}"


