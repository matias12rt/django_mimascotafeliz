from django.urls import path
<<<<<<< Updated upstream
from .views import index, validar_cuenta, registro

urlpatterns = [
    path('', index, name='index'),
    path('validar_cuenta/', validar_cuenta, name='validar_cuenta'),
    path('registro', registro, name='registro')
=======
from .views import actualizar_cantidad, add_to_cart, editarC, editarG, eliminar_boleta, eliminarC, index, listCategoria, pagar_carrito, tienda_invitado, eliminarG, listgenero, eliminarCuen, vaciar_carrito, ventas, registro, registro_admin, crudAdmin, agregarpro, producto_del, producto_edit, productoUpdate, ver_boletas

urlpatterns = [
    path('', index, name='index'),
    
    path('boletas', ver_boletas, name='boletas'),
    path('boletas/<int:id_vol_fact>/', eliminar_boleta, name='eliminar_boleta'),
    path('add_to_cart/', add_to_cart, name='add_to_cart'),
    path('listCategoria/', listCategoria, name='listCategoria'),
    path('editarG/<int:pk>/', editarG, name='editarG'),
    path('editarC/<int:pk>/', editarC, name='editarC'),
    path('eliminarC/<int:pk>/', eliminarC, name='eliminarC'),
    path('listgenero', listgenero, name='listgenero'),
    path('eliminarG/<int:pk>/', eliminarG, name='eliminarG'),
    path('eliminarCuen/', eliminarCuen, name='eliminarCuen'),
    path('tienda_invitado', tienda_invitado, name='tienda_invitado'),
    path('registro', registro, name='registro'),
    path('ventas', ventas, name='ventas'),
    path('vaciar_carrito/', vaciar_carrito, name='vaciar_carrito'),
    path('actualizar_cantidad/', actualizar_cantidad, name='actualizar_cantidad'),
    path('pagar_carrito/', pagar_carrito, name='pagar_carrito'),
    path('registro_admin/', registro_admin, name='registro_admin'),
    path('crudAdmin/', crudAdmin, name='crudAdmin'),
    path('agregarpro', agregarpro, name='agregarpro'),
    path('producto_del/<str:pk>', producto_del, name='producto_del'),
    path('producto_edit/<str:pk>', producto_edit, name='producto_edit'),
    path('productoUpdate', productoUpdate, name='productoUpdate')
>>>>>>> Stashed changes
]