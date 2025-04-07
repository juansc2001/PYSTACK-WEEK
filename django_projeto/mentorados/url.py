from django.urls import path
from .views import mentorados
urlpatterns = [
    path('', mentorados, name = 'mentorados')
]