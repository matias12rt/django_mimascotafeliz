import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import  render
from .models import RegistroAdmin, RegistroCuenta, CuentaCliente, Genero, Producto, CategoriaPro
# Create your views here.
def registro_admin (request):
    return render (request, 'mascota/registro_admin.html')
    
def index(request):
    return render(request, 'mascota/index.html')

def ventas(request):
    productos = Producto.objects.all()
    categorias = CategoriaPro.objects.all()

    query = request.GET.get('q')
    categoria_id = request.GET.get('categoria')

    if query:
        productos = productos.filter(nombre_pro__icontains=query) | productos.filter(codigo__icontains=query)

    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

    return render(request, 'mascota/ventas.html', {
        'productos': productos,
        'categorias': categorias,
        'query': query,
        'categoria_id': categoria_id
    })



def crud(request):
    productos = Producto.objects.all()
    context = {'productos': productos}
    return render(request, 'mascota/admin.html', context)

def productoUpdate(request):
    if request.method == "POST":
        codigo_pro=request.POST["product_code"]    
        nombre_pro_p= request.POST["nom_producto"]
        descripcion_pro_p=request.POST["pro_descripcion"]
        valor_pro_p=request.POST["product_valor"]
        categoria_p=request.POST["pro_categoria"]
        imagen_p=request.POST["product_image"]

        objCategoria=CategoriaPro.objects.get(id_categoria = categoria_p)

        productos = Producto()
        productos.codigo = codigo_pro,
        productos.nombre_pro = nombre_pro_p,
        productos.descripcion_pro = descripcion_pro_p,
        productos.valor_pro =  valor_pro_p,
        productos.categoria = objCategoria,
        productos.imagen = imagen_p
        productos.save()

        categoria=CategoriaPro.objects.all()
        context={'mensaje': "datos actualizados...", 'categoria': categoria, 'productos': productos}
        return render(request, 'mascota/edit_pro.html', context)
    else:
        productos = Producto.objects.all()
        context={'productos':productos}
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
def agregarpro(request):
    if request.method is not "POST":
        categoria=CategoriaPro.objects.all()
        context={'categoria': categoria}
        return render(request, 'mascota/ingresopro.html', context)
    else:
        codigo_pro=request.POST["product_code"]    
        nombre_pro_p= request.POST["nom_producto"]
        descripcion_pro_p=request.POST["pro_descripcion"]
        valor_pro_p=request.POST["product_valor"]
        categoria_p=request.POST["pro_categoria"]
        imagen_p=request.POST["product_image"]
    

        objCategoria=CategoriaPro.objects.get(id_categoria = categoria_p)
        obj=Producto.objects.create( codigo = codigo_pro,
                                    nombre_pro = nombre_pro_p,
                                    descripcion_pro = descripcion_pro_p,
                                    valor_pro =  valor_pro_p,
                                    categoria = objCategoria,
                                    imagen = imagen_p,
                                    )
        obj.save()
        context={'mensaje': "Producto ingresado"}
        return render(request, 'mascota/ingresopro.html', context)
        



def registro(request):
    if request.method == "POST":
        # Obtener datos del formulario
        nombre = request.POST["nombre"]
        apellido = request.POST["apellido"]
        gmail_cli = request.POST["gmail"]
        direccion_cli = request.POST["direccion"]
        clave_cli = request.POST["password"]
        genero_id = request.POST["sexo"]

        # Obtener objeto de género
        try:
            objGenero = Genero.objects.get(id_genero=genero_id)
        except Genero.DoesNotExist:
            objGenero = None
            # Puedes manejar aquí el caso de género no encontrado

        # Crear objeto CuentaCliente si el género existe
        if objGenero:
            obj = CuentaCliente.objects.create(
                nombre_cli=nombre,
                apellido_cli=apellido,
                gmail=gmail_cli,
                direccion=direccion_cli,
                clave=clave_cli,
                genero=objGenero
            )
            obj.save()
            mensaje = "Datos guardados correctamente."
        else:
            mensaje = "Error: Género no encontrado."

        context = {'mensaje': mensaje}
        return render(request, 'mascota/registro.html', context)

    else:
        # Si el método no es POST, cargar los géneros disponibles
        generos = Genero.objects.all()
        context = {'generos': generos}
        return render(request, 'mascota/registro.html', context)
    


def validar_cuenta(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        email = data.get('email')
        password = data.get('password')

        response_data = {
            'valid': False,
            'error_type': '',
            'is_admin': False,
        }

        try:
            admin = RegistroAdmin.objects.get(gmail_admin=email)
            if admin.clave_admin == password:
                response_data['valid'] = True
                response_data['is_admin'] = True
            else:
                response_data['error_type'] = 'invalid_password'
        except RegistroAdmin.DoesNotExist:
            try:
                cuenta = RegistroCuenta.objects.get(gmail_cuenta=email)
                if cuenta.clave_cuenta == password:
                    response_data['valid'] = True
                else:
                    response_data['error_type'] = 'invalid_password'
            except RegistroCuenta.DoesNotExist:
                response_data['error_type'] = 'email_not_registered'

        return JsonResponse(response_data)

    return render(request, 'mascota/index.html')