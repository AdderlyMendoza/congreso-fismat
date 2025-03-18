from django.db import models
from registro.models import Registro

class Asistencia(models.Model):
    usuario = models.ForeignKey(Registro, on_delete=models.CASCADE)
    entrada = models.DateTimeField(null=True, blank=True)  # Cambiado de DateTimeField a DateField
    salida = models.DateTimeField(null=True, blank=True)  # Cambiado de DateTimeField a DateField
    fecha = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'fecha')  # Asegura que solo haya un registro por día

    def __str__(self):
        # Concatenamos todos los campos en un solo string
        return f"id: {self.usuario.id}, DNI: {self.usuario.dni}, Nombres: {self.usuario.nombres}, Apellido Paterno: {self.usuario.apellido_paterno}, " \
               f"Apellido Materno: {self.usuario.apellido_materno}"
