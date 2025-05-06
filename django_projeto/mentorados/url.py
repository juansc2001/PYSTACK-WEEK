from django.urls import path
from .views import mentorados, abrirhorarios
urlpatterns = [
    path('', mentorados, name = 'mentorados'),
    path('reunioes/', abrirhorarios, name = 'marcar_reunioes')
]