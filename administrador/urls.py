from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index-inscritos'),
    path('inscritos', views.lista_inscritos, name='lista-inscritos'),
    path('pdf', views.ver_pdf, name='pdf'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
