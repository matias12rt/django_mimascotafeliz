from django.urls import path
from .views import index, validar_cuenta, ventas, registro, registro_admin, crud, agregarpro, producto_del, producto_edit, productoUpdate

urlpatterns = [
    path('', index, name='index'),
    path('validar_cuenta/', validar_cuenta, name='validar_cuenta'),
    path('registro', registro, name='registro'),
    path('ventas', ventas, name='ventas'),
    path('admins', registro_admin, name='admins'),
    path('crud', crud, name='crud'),
    path('agregrapro', agregarpro, name='agregarpro'),
    path('producto_del/<str:pk>', producto_del, name='producto_del'),
    path('producto_edit/<str:pk>', producto_edit, name='producto_edit'),
    path('productoUpdate', productoUpdate, name='productoUpdate')
]