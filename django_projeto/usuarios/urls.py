from django.urls import path
from . import views

urlpatterns = [
    path('cadastro/', views.cadastro, name= 'cadastro'), #primeiro parametro é a url
    path('loguin/', views.loguin, name= 'loguin'),
]