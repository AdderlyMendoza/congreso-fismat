from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

from django.contrib.auth.decorators import login_required


urlpatterns = [
    
    path('', login_required(views.index), name='index-inscritos'),
    path('inscritos', login_required(views.lista_inscritos), name='lista-inscritos'),
    path('validar-inscrito/<int:id>/', login_required(views.validar_inscrito), name='validar-inscrito'),
    
    # path('pdf', views.ver_pdf, name='pdf'),
    
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
