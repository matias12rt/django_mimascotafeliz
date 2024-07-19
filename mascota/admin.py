from django.contrib import admin
from .models import Producto, CategoriaPro, Genero, CuentaAdmin, CuentaCliente, RegistroCuenta, FacturaBoleta, RegistroAdmin

# Registrar los modelos en el administrador
admin.site.register(Producto)
admin.site.register(CategoriaPro)
admin.site.register(Genero)
admin.site.register(CuentaAdmin)
admin.site.register(CuentaCliente)
admin.site.register(RegistroCuenta)
admin.site.register(FacturaBoleta)
admin.site.register(RegistroAdmin)