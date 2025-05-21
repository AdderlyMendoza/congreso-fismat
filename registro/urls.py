from django.urls import path
from . import views  # Importa las vistas de la app 'registro'

urlpatterns = [
    
    path('', views.registro_view, name='registro_form'),  # Ruta del formulario de registro
    path('validar-duplicados/', views.validar_duplicados, name='validar_duplicados'),  # Nueva ruta para validar duplicados
    path('registro-constancia/<str:dni>/', views.registro_constancia, name='registro_constancia'),  # Ruta para generar la constancia de registro
    path('generar-pdf/<str:dni>/', views.generar_pdf, name='generar_pdf'),

]
