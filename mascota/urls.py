from django.urls import path
from .views import index, validar_cuenta, registro

urlpatterns = [
    path('', index, name='index'),
    path('validar_cuenta/', validar_cuenta, name='validar_cuenta'),
    path('registro', registro, name='registro')
]