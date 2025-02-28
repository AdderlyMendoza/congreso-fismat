from django.urls import path
from . import views  # Importa las vistas de la app 'web'

urlpatterns = [
    path('', views.index, name='page_admin'),  # Ruta de la landing page
]
