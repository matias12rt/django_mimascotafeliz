from django.db import models

def product_image_upload_path(instance, filename):
    return f'productos/{filename}'

class Genero(models.Model):
    id_genero = models.AutoField(primary_key=True)
    genero = models.CharField(max_length=100)

    def __str__(self):
        return self.genero

class CuentaAdmin(models.Model):
    id_admin = models.AutoField(primary_key=True)
    nombre_admin = models.CharField(max_length=100)
    apellido_admin = models.CharField(max_length=100)
    gmail_admin = models.EmailField(unique=True)
    direccion_admin = models.CharField(max_length=255)
    clave_admin = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.nombre_admin} {self.apellido_admin}"

class CategoriaPro(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre_cate = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_cate

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=20, unique=True)  # Nuevo campo para el código del producto
    nombre_pro = models.CharField(max_length=100)
    descripcion_pro = models.TextField()
    valor_pro = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey('CategoriaPro', on_delete=models.CASCADE, related_name='productos')
    imagen = models.ImageField(upload_to=product_image_upload_path, blank=True, null=True)

    def __str__(self):
        return self.nombre_pro

class CuentaCliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nombre_cli = models.CharField(max_length=100)
    apellido_cli = models.CharField(max_length=100)
    gmail = models.EmailField(unique=True)
    direccion = models.CharField(max_length=255)
    clave = models.CharField(max_length=255)
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE, related_name='clientes')

    def __str__(self):
        return f"{self.nombre_cli} {self.apellido_cli}"

class RegistroCuenta(models.Model):
    id_cuenta = models.AutoField(primary_key=True)
    gmail_cuenta = models.EmailField(unique=True)
    clave_cuenta = models.CharField(max_length=255)
    cuenta_cliente = models.OneToOneField(CuentaCliente, on_delete=models.CASCADE, related_name='registro_cuenta')

    def __str__(self):
        return self.gmail_cuenta

class FacturaBoleta(models.Model):
    id_vol_fact = models.AutoField(primary_key=True)
    nombre_cli = models.CharField(max_length=100)
    apellido_cli = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    gmail_cli = models.EmailField()
    productos = models.ManyToManyField(Producto, related_name='facturas')
    cliente = models.ForeignKey(CuentaCliente, on_delete=models.CASCADE, related_name='facturas')

    def __str__(self):
        return f"Factura {self.id_vol_fact} - {self.nombre_cli} {self.apellido_cli}"
