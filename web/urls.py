from django.urls import path
from . import views  # Importa las vistas de la app 'web'

urlpatterns = [
    path('', views.landing_page, name='landing_page'),  # Ruta de la landing page
    path('bases-cientificas', views.bases_cientificas, name='bases-cientificas'),  # Ruta de la landing page
]
