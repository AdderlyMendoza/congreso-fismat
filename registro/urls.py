from django.urls import path
from . import views  # Importa las vistas de la app 'registro'

urlpatterns = [
    path('', views.registro_view, name='registro_form'),  # Ruta del formulario de registro
]
