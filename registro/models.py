from django.db import models

class Registro(models.Model):
    dni = models.CharField(max_length=8, blank=True, null=True)
    nombres = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    email = models.EmailField()
    celular = models.CharField(max_length=15, blank=True, null=True)
    # proyecto_investigacion = models.FileField(upload_to='pdfs/')  # Esta carpeta almacenará los archivos PDF
    proyecto_investigacion = models.FileField(upload_to='pdfs/', blank=False, null=True)  # Hacerlo opcional
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Concatenamos todos los campos en un solo string
        return f"DNI: {self.dni}, Nombres: {self.nombres}, Apellido Paterno: {self.apellido_paterno}, " \
               f"Apellido Materno: {self.apellido_materno}, Email: {self.email}, Celular: {self.celular}, " \
               f"Proyecto: {self.proyecto_investigacion}, Fecha de Registro: {self.fecha_registro}"

