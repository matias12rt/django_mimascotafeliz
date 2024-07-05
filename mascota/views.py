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