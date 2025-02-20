from django.db import models

class Registro(models.Model):
    dni = models.CharField(max_length=8, blank=True, null=True)
    nombres = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    email = models.EmailField()
    celular = models.CharField(max_length=15, blank=True, null=True)
    proyecto_investigacion = models.FileField(upload_to='pdfs/')  # Esta carpeta almacenará los archivos PDF
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.email}"


