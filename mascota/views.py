<<<<<<< Updated upstream
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import RegistroCuenta, CuentaAdmin

# Create your views here.
def index(request):

    return render(request, 'mascota/index.html')

def registro(request):
    
    return render(request, 'mascota/registro.html')

@csrf_exempt
def validar_cuenta(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email', '')
        password = data.get('password', '')

        try:
            # Verificar si existe la cuenta en RegistroCuenta (clientes)
            cuenta_cliente = RegistroCuenta.objects.get(gmail_cuenta=email)
            if cuenta_cliente.clave_cuenta == password:
                return JsonResponse({'valid': True, 'is_admin': False})
            else:
                return JsonResponse({'valid': False, 'error_type': 'invalid_password'})

        except RegistroCuenta.DoesNotExist:
            try:
                # Verificar si existe la cuenta en CuentaAdmin (administradores)
                cuenta_admin = CuentaAdmin.objects.get(gmail_admin=email)
                if cuenta_admin.clave_admin == password:
                    return JsonResponse({'valid': True, 'is_admin': True})
                else:
                    return JsonResponse({'valid': False, 'error_type': 'invalid_password'})

            except CuentaAdmin.DoesNotExist:
                return JsonResponse({'valid': False, 'error_type': 'email_not_registered'})

    return JsonResponse({'error': 'Método no permitido'}, status=405)
=======
from django.forms import ValidationError
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import  get_object_or_404, redirect, render
from .utils import admin_required
from .models import Carrito, CarritoItem, CuentaAdmin, CuentaCliente, FacturaBoleta, Genero, Producto, CategoriaPro, RegistroAdmin, RegistroCuenta
# Create your views here.

def registro(request):
    if request.method != "POST":
        generos = Genero.objects.all()
        context = {'generos': generos}
        return render(request, 'mascota/registro.html', context)
    else:
        nombre = request.POST["nombre"]
        apellido = request.POST["apellido"]
        gmail = request.POST["gmail"]
        direccion = request.POST["direccion"]
        contraseña = request.POST["password"]
        genero = request.POST["sexo"]

        # Validación de nombre y apellido
        if not nombre.isalpha() or len(nombre) < 3:
            generos = Genero.objects.all()
            context = {
                'generos': generos,
                'modal_error': "El nombre debe tener solo letras y al menos 3 caracteres."
            }
            return render(request, 'mascota/registro.html', context)

        if not apellido.isalpha() or len(apellido) < 3:
            generos = Genero.objects.all()
            context = {
                'generos': generos,
                'modal_error': "El apellido debe tener solo letras y al menos 3 caracteres."
            }
            return render(request, 'mascota/registro.html', context)

        # Verificación de correo existente
        if CuentaCliente.objects.filter(gmail=gmail).exists():
            generos = Genero.objects.all()
            context = {
                'generos': generos,
                'modal_error': "El correo ingresado ya está registrado, intente con otro."
            }
            return render(request, 'mascota/registro.html', context)

        try:
            objGenero = Genero.objects.get(id_genero=genero)
            # Crear la cuenta del cliente
            cuenta_cliente = CuentaCliente.objects.create(
                nombre_cli=nombre,
                apellido_cli=apellido,
                gmail=gmail,
                direccion=direccion,
                clave=contraseña,
                genero=objGenero,
            )

            # Crear el registro en RegistroCuenta
            RegistroCuenta.objects.create(
                gmail_cuenta=gmail,
                clave_cuenta=contraseña,
                cuenta_cliente=cuenta_cliente
            )

            generos = Genero.objects.all()
            context = {
                'generos': generos,
                'modal_success': "Registro exitoso, ya puede utilizar su cuenta.",
                'registro_exitoso': True  # Indicador para mostrar el modal
            }
            return render(request, 'mascota/registro.html', context)

        except ValidationError as e:
            generos = Genero.objects.all()
            context = {
                'generos': generos,
                'modal_error': e.messages
            }
            return render(request, 'mascota/registro.html', context)
        except Exception as e:
            # Manejo de cualquier otro error
            generos = Genero.objects.all()
            context = {
                'generos': generos,
                'modal_error': "Ocurrió un error, por favor intente nuevamente."
            }
            return render(request, 'mascota/registro.html', context)
    
def registro_admin(request):
    if request.method != "POST":
        return render(request, 'mascota/registro_admin.html')
    else:
        nombre = request.POST["nombre"]
        apellido = request.POST["apellido"]
        gmail = request.POST["gmail"].strip()
        direccion = request.POST["direccion"]
        clave = request.POST["password"]

        # Validación de nombre y apellido
        if not nombre.isalpha() or len(nombre) < 3:
            return JsonResponse({'modal_error': "El nombre debe tener solo letras y al menos 3 caracteres."})

        if not apellido.isalpha() or len(apellido) < 3:
            return JsonResponse({'modal_error': "El apellido debe tener solo letras y al menos 3 caracteres."})

        # Verificación de correo existente
        if CuentaAdmin.objects.filter(gmail_admin=gmail).exists():
            return JsonResponse({'modal_error': "El correo ingresado ya está registrado, intente con otro."})

        # Crear nuevo registro de administrador
        try:
            # Crear la cuenta de administrador
            cuenta_admin = CuentaAdmin.objects.create(
                nombre_admin=nombre,
                apellido_admin=apellido,
                gmail_admin=gmail,
                direccion_admin=direccion,
                clave_admin=clave
            )

            # Crear el registro en RegistroAdmin
            RegistroAdmin.objects.create(
                gmail_admin=gmail,
                clave_admin=clave,
                cuenta_admin=cuenta_admin
            )

            return JsonResponse({'modal_success': "Registro exitoso, ya puede utilizar su cuenta."})
        except ValidationError as e:
            return JsonResponse({'modal_error': str(e)})
        except Exception as e:
            return JsonResponse({'modal_error': "Ocurrió un error, por favor intente nuevamente."})
    
def index(request):
    if request.method == "POST":
        email = request.POST.get('email', '').strip()
        contraseña = request.POST.get('contraseña', '').strip()

        # Verificar en RegistroCuenta
        try:
            registro_cliente = RegistroCuenta.objects.get(gmail_cuenta=email)
            if registro_cliente.clave_cuenta == contraseña:
                request.session['user_id'] = registro_cliente.id_cuenta
                return JsonResponse({'redirect_url': 'ventas'})
            else:
                return JsonResponse({'error': 'Contraseña incorrecta.'}, status=400)
        except RegistroCuenta.DoesNotExist:
            pass  # Continuar a la siguiente verificación

        # Verificar en RegistroAdmin
        try:
            registro_admin = RegistroAdmin.objects.get(gmail_admin=email)
            if registro_admin.clave_admin == contraseña:
                request.session['admin_id'] = registro_admin.id_registro_admin
                return JsonResponse({'redirect_url': 'crudAdmin'})
            else:
                return JsonResponse({'error': 'Contraseña incorrecta.'}, status=400)
        except RegistroAdmin.DoesNotExist:
            return JsonResponse({'error': 'El email ingresado no se encuentra registrado.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f"Error inesperado: {e}"}, status=500)

    return render(request, 'mascota/index.html')

def tienda_invitado(request):
    productos = Producto.objects.all()
    categorias = CategoriaPro.objects.all()

    query = request.GET.get('q')
    categoria_id = request.GET.get('categoria')

    # Aplicar búsqueda
    if query:
        productos = productos.filter(nombre_pro__icontains=query) | productos.filter(codigo__icontains=query)

    # Aplicar filtrado por categoría
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

    return render(request, 'mascota/ventas_invitado.html', {
        'productos': productos,
        'categorias': categorias,
        'query': query,
        'categoria_id': categoria_id
    })

def ver_boletas(request):
    boletas = FacturaBoleta.objects.all()
    context={'boletas': boletas}
    return render(request, 'mascota/boletas.html', context)

def eliminar_boleta(request, id_vol_fact):
    boleta = get_object_or_404(FacturaBoleta, id_vol_fact=id_vol_fact)
    boleta.delete()
    return redirect('boletas')

def ventas(request):
    productos = Producto.objects.all()
    categorias = CategoriaPro.objects.all()
    query = request.GET.get('q')
    categoria_id = request.GET.get('categoria')

    if query:
        productos = productos.filter(nombre_pro__icontains=query) | productos.filter(codigo__icontains=query)
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

    # Obtener el carrito del usuario
    try:
        registro_cuenta = RegistroCuenta.objects.get(gmail_cuenta=request.user.email)
    except RegistroCuenta.DoesNotExist:
        return render(request, 'mascota/ventas.html', {
            'productos': productos,
            'categorias': categorias,
            'query': query,
            'categoria_id': categoria_id,
            'carrito_items': []
        })
    
    carrito, created = Carrito.objects.get_or_create(usuario = registro_cuenta)
    
    carrito_items = CarritoItem.objects.filter(carrito=carrito)

    return render(request, 'mascota/ventas.html', {
        'productos': productos,
        'categorias': categorias,
        'query': query,
        'categoria_id': categoria_id,
        'carrito_items': carrito_items
    })

def vaciar_carrito(request):
    try:
        registro_cuenta = RegistroCuenta.objects.get(gmail_cuenta=request.user.email)
    except RegistroCuenta.DoesNotExist:
        return JsonResponse({'status': 'fail', 'message': 'No se encontró el registro de cuenta'})
    
    carrito, created = Carrito.objects.get_or_create(usuario=registro_cuenta)
    carrito.carritoitem_set.all().delete()  # Elimina todos los ítems del carrito
    
    return JsonResponse({'status': 'ok', 'message': 'Carrito vacío'})

@login_required
def pagar_carrito(request):
    if request.method == 'POST':
        try:
            registro_cuenta = RegistroCuenta.objects.get(gmail_cuenta=request.user.email)
        except RegistroCuenta.DoesNotExist:
            return JsonResponse({'status': 'fail', 'message': 'No se encontró el registro de cuenta'})
        
        carrito, created = Carrito.objects.get_or_create(usuario=registro_cuenta)
        carrito_items = CarritoItem.objects.filter(carrito=carrito)
        
        if not carrito_items.exists():
            return JsonResponse({'status': 'fail', 'message': 'El carrito está vacío'})
        
        factura = FacturaBoleta(
            nombre_cli=registro_cuenta.cuenta_cliente.nombre_cli,
            apellido_cli=registro_cuenta.cuenta_cliente.apellido_cli,
            direccion=registro_cuenta.cuenta_cliente.direccion,
            gmail_cli=registro_cuenta.gmail_cuenta,
            cliente=registro_cuenta.cuenta_cliente
        )
        factura.save()
        factura.productos.set(carrito_items.values_list('producto', flat=True))
        
        carrito_items.delete()  # Vaciar el carrito después del pago
        
        return JsonResponse({'status': 'ok', 'message': 'Pago realizado con éxito'})
    
    return JsonResponse({'status': 'fail', 'message': 'Método no permitido'})
def actualizar_cantidad(request):
    if request.method == 'POST':
        producto_id = request.POST.get('producto_id')
        nueva_cantidad = int(request.POST.get('cantidad'))
        
        if not producto_id or nueva_cantidad <= 0:
            return JsonResponse({'status': 'fail', 'message': 'Datos inválidos'})
        
        producto = get_object_or_404(Producto, id_producto=producto_id)
        try:
            registro_cuenta = RegistroCuenta.objects.get(gmail_cuenta=request.user.email)
        except RegistroCuenta.DoesNotExist:
            return JsonResponse({'status': 'fail', 'message': 'No se encontró el registro de cuenta'})
        
        carrito, created = Carrito.objects.get_or_create(usuario=registro_cuenta)
        carrito_item, created = CarritoItem.objects.get_or_create(carrito=carrito, producto=producto)
        
        carrito_item.cantidad = nueva_cantidad
        carrito_item.save()

        return JsonResponse({
            'status': 'ok',
            'producto_nombre': producto.nombre_pro,
            'cantidad': carrito_item.cantidad
        })
    
    return JsonResponse({'status': 'fail', 'message': 'Método no permitido'})
@login_required
def add_to_cart(request):
    if request.method == 'POST':
        producto_id = request.POST.get('producto_id')
        
        if not producto_id:
            return JsonResponse({'status': 'fail', 'message': 'No se proporcionó un ID de producto'})
        
        producto = get_object_or_404(Producto, id_producto=producto_id)
        
        try:
            registro_cuenta = RegistroCuenta.objects.get(gmail_cuenta=request.user.email)
        except RegistroCuenta.DoesNotExist:
            return JsonResponse({'status': 'fail', 'message': 'No se encontró el registro de cuenta'})
        
        # Obtener o crear el carrito para el usuario
        carrito, created = Carrito.objects.get_or_create(usuario=registro_cuenta)
        
        # Obtener o crear el item en el carrito
        carrito_item, created = CarritoItem.objects.get_or_create(carrito=carrito, producto=producto)
        
        if created:
            carrito_item.cantidad = 1
        else:
            carrito_item.cantidad += 1
        
        carrito_item.save()

        return JsonResponse({
            'status': 'ok',
            'producto_nombre': producto.nombre_pro,
            'cantidad': carrito_item.cantidad
        })
    
    return JsonResponse({'status': 'fail', 'message': 'Método no permitido'})

@admin_required
def crudAdmin(request):
    productos = Producto.objects.all()
    context = {'productos': productos}
    return render(request, 'mascota/admin.html', context)


def productoUpdate(request):
    if request.method == "POST":
        codigo_pro = request.POST["product_code"]    
        nombre_pro_p = request.POST["nom_producto"]
        descripcion_pro_p = request.POST["pro_descripcion"]
        valor_pro_p = request.POST["product_valor"]
        categoria_p = request.POST["pro_categoria"]
        imagen_p = request.FILES["product_image"]

        objCategoria = CategoriaPro.objects.get(id_categoria=categoria_p)

        # Asumiendo que `codigo_pro` es el identificador único del producto que quieres actualizar
        productos = Producto.objects.get(codigo=codigo_pro)
        
        productos.nombre_pro = nombre_pro_p
        productos.descripcion_pro = descripcion_pro_p
        productos.valor_pro = valor_pro_p
        productos.categoria = objCategoria
        if imagen_p:  # Solo actualiza la imagen si se proporciona una nueva
            productos.imagen = imagen_p
        productos.save()

        categoria = CategoriaPro.objects.all()
        context = {'mensaje': "datos actualizados...", 'categoria': categoria, 'productos': productos}
        return render(request, 'mascota/edit_pro.html', context)
    else:
        productos = Producto.objects.all()
        context = {'productos': productos}
        return render(request, 'mascota/admin.html', context)


def producto_edit(request, pk):

    if pk!= "":
        productos = Producto.objects.get(codigo = pk)
        categoria=CategoriaPro.objects.all()

        print(type(productos.categoria.id_categoria))

        context={'productos': productos, 'categoria': categoria}
        if productos:
            return render(request, 'mascota/edit_pro.html', context)
        else:
            context={'mensaje': "error, codigo no existe..."}
            return render(request, 'mascota/edit_pro.html', context)


def producto_del(request, pk):
    context={}
    try:
        producto=Producto.objects.get(codigo=pk)


        producto.delete()
        mensaje="bien, datos eliminados..."
        productos = Producto.objects.all()
        context = {'productos': productos, 'mensaje':mensaje}
        return render(request, 'mascota/admin.html', context)
    except:
        mensaje="Error, codigo de producto no encontrado..."
        productos = Producto.objects.all()
        context = {'productos': productos, 'mensaje':mensaje}
        return render(request, 'mascota/admin.html', context)

def eliminarC(request, pk):
    if request.method == "POST":
        try:
            categoria = CategoriaPro.objects.get(id_categoria=pk)
            categoria.delete()
            return JsonResponse({'success': True, 'mensaje': "Bien, categoría eliminada..."})
        except CategoriaPro.DoesNotExist:
            return JsonResponse({'success': False, 'mensaje': "Error, categoría no encontrada"})
        except Exception as e:
            return JsonResponse({'success': False, 'mensaje': "Error al eliminar: " + str(e)})
    else:
        return JsonResponse({'success': False, 'mensaje': "Método no permitido"})
    
def editarG(request, pk):
    if request.method == "POST":
        nuevo_nombre = request.POST.get('nombre_genero').strip()
        try:
            genero = Genero.objects.get(id_genero=pk)
            genero.genero = nuevo_nombre
            genero.save()
            return JsonResponse({'success': True, 'mensaje': "Género actualizado."})
        except Genero.DoesNotExist:
            return JsonResponse({'success': False, 'mensaje': "Género no encontrado."})
        except Exception as e:
            return JsonResponse({'success': False, 'mensaje': "Error al actualizar: " + str(e)})
    else:
        return JsonResponse({'success': False, 'mensaje': "Método no permitido"})
    
def editarC(request, pk):
    if request.method == "POST":
        nuevo_nombre = request.POST.get('nombre_categoria').strip()
        try:
            categoria = CategoriaPro.objects.get(id_categoria=pk)
            categoria.nombre_cate = nuevo_nombre
            categoria.save()
            return JsonResponse({'success': True, 'mensaje': "Categoría actualizada."})
        except CategoriaPro.DoesNotExist:
            return JsonResponse({'success': False, 'mensaje': "Categoría no encontrada."})
        except Exception as e:
            return JsonResponse({'success': False, 'mensaje': "Error al actualizar: " + str(e)})
    else:
        return JsonResponse({'success': False, 'mensaje': "Método no permitido"})

def listCategoria(request):
    if request.method == "POST":
        nombre_categoria = request.POST["nom_categoria"].strip()

        # Validar si la categoría ya existe
        if CategoriaPro.objects.filter(nombre_cate=nombre_categoria).exists():
            return JsonResponse({'success': False, 'mensaje': "Esta categoría ya existe."})

        try:
            obj = CategoriaPro.objects.create(nombre_cate=nombre_categoria)
            obj.save()
            return JsonResponse({'success': True, 'mensaje': "Categoría ingresada", 'categoria': {'id_categoria': obj.id_categoria, 'nombre_cate': obj.nombre_cate}})
        except Exception as e:
            return JsonResponse({'success': False, 'mensaje': "No ingresada: " + str(e)})
    else:
        categorias = CategoriaPro.objects.all()
        context = {'categorias': categorias}
        return render(request, 'mascota/Categoria.html', context)

def eliminarG(request, pk):
    if request.method == "POST":
        try:
            genero = Genero.objects.get(id_genero=pk)
            genero.delete()
            return JsonResponse({'success': True, 'mensaje': "Bien, género eliminado..."})
        except Genero.DoesNotExist:
            return JsonResponse({'success': False, 'mensaje': "Error, género no encontrado"})
        except Exception as e:
            return JsonResponse({'success': False, 'mensaje': "Error al eliminar: " + str(e)})
    else:
        return JsonResponse({'success': False, 'mensaje': "Método no permitido"})
    
def listgenero(request):
    if request.method == "POST":
        nombre_genero = request.POST["nom_genero"].strip()

        # Validar si el género ya existe
        if Genero.objects.filter(genero=nombre_genero).exists():
            return JsonResponse({'success': False, 'mensaje': "Este género ya existe."})

        try:
            obj = Genero.objects.create(genero=nombre_genero)
            obj.save()
            return JsonResponse({'success': True, 'mensaje': "Género ingresado", 'genero': {'id_genero': obj.id_genero, 'genero': obj.genero}})
        except Exception as e:
            return JsonResponse({'success': False, 'mensaje': "No ingresado: " + str(e)})
    else:
        generos = Genero.objects.all()
        context = {'generos': generos}
        return render(request, 'mascota/Generos.html', context)

def eliminarCuen(request):
    if request.method == 'POST':
        cor = request.POST.get('email')
        try:
            cuenta = CuentaCliente.objects.get(gmail=cor)
            cuenta.delete()
            return JsonResponse({'success': True, 'mensaje': "Cuenta eliminada con éxito."})
        except CuentaCliente.DoesNotExist:
            return JsonResponse({'success': False, 'mensaje': "Error, el correo no es correcto o no está registrado."})
    else:
        return JsonResponse({'success': False, 'mensaje': "Método no permitido."})



def agregarpro(request):
    if request.method != "POST":
        categoria = CategoriaPro.objects.all()
        context = {'categoria': categoria}
        return render(request, 'mascota/ingresopro.html', context)
    else:
        try:
            codigo_pro = request.POST["product_code"]
            nombre_pro_p = request.POST["nom_producto"]
            descripcion_pro_p = request.POST["pro_descripcion"]
            valor_pro_p = request.POST["product_valor"]
            categoria_p = request.POST["pro_categoria"]
            imagen_p = request.FILES["product_image"]

            objCategoria = CategoriaPro.objects.get(id_categoria=categoria_p)
            obj = Producto.objects.create(
                codigo=codigo_pro,
                nombre_pro=nombre_pro_p,
                descripcion_pro=descripcion_pro_p,
                valor_pro=valor_pro_p,
                categoria=objCategoria,
                imagen=imagen_p,
            )
            obj.save()
            context = {'mensaje': "Producto ingresado", 'modal_success': True}
        except Exception as e:
            context = {'mensaje': f"Error al ingresar el producto: {str(e)}", 'modal_error': True}

        return render(request, 'mascota/ingresopro.html', context)

        


>>>>>>> Stashed changes
