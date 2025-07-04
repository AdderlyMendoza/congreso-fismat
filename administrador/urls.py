from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

from django.contrib.auth.decorators import login_required


urlpatterns = [
    
    path('', login_required(views.index), name='index-inscritos'),
    
    path('inscritos', login_required(views.lista_inscritos), name='lista-inscritos'),
    path('validar-inscrito/<int:id>/', login_required(views.validar_inscrito), name='validar-inscrito'),

    # Eliminar y editar registro
    path('eliminar-inscrito/<int:id>/', login_required(views.eliminar_inscrito), name='eliminar-inscrito'),
    path('editar-voucher/<int:id>', login_required(views.editar_imagen), name='editar-imagen'),

    path('excel-inscritos-validados', login_required(views.excel_inscritos_validados), name='excel-inscritos-validados'),

    
    # ASISTENCIA
    path('entrada', login_required(views.entrada_inscritos), name='entrada-inscritos'),
    path('salida', login_required(views.salida_inscritos), name='salida-inscritos'),
    
    
    # path('pdf', views.ver_pdf, name='pdf'),
    
    # ADMINISTAR USUARIOS(ADMINISTRADORES)
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register-admin-2025/', views.register_view, name='register'),
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
