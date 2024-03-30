from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash


def user_validate(request):
    print("Inicio de la función user_validate")
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        print("Si es un metodo POST")
        print(request.POST)

        if form.is_valid():
            print("Entro a la validacion del form")
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print("Se autentifico")
            # Intenta autenticar al usuario sin considerar si está activo o no
            user = authenticate(username=username, password=password)
            
            if user and user.is_active:
                print("Usuario validado")
                if password == 'ZensorialSpa2024*':  # Esta línea necesita revisión para seguridad
                        print("Contraseña por defecto reconocida, redirigiendo a index")
                        messages.success(request,"Usuario existente, cambia tu contraseña")
                        return redirect('index')
                else:
                    print("Usuario valido, ya cambio su contraseña")
                    messages.success(request,"Usuario y contraseña correctos.")
                    return redirect('home')
            else:
                print("El Usuario no esta activo")
                messages.success(request, "Usuario Inactivo")
                return redirect('login')
        else:
            print("Formulario no válido")
            print(form.errors)

        messages.error(request, "Información de inicio de sesión inválida.")
        return redirect('login')
    else:
        print("Método no es POST")
        form = AuthenticationForm()
        return redirect('login')
# Vistas del cambio de contraseña
def pass_view(request):
 return render(request,'intranet/cambio_contrasena_form.html')
def activate_view(request):
 return render(request,'intranet/index.html')

def ficha_view(request):
 return render(request,'intranet/ficha.html')

def login_view(request):
 return render(request,'intranet/login.html')

def home_view(request):
 return render(request,'intranet/home.html')

def cita_view(request):
 return render(request,'intranet/cita.html')
def ficha_view(request):
 return render(request,'intranet/ficha.html')

@login_required
@permission_required('app.permission_code', raise_exception=True)
def mi_vista(request):
    return # Código de la vista

def password_complex(password):
    """
    Esta función valida si la contraseña cumple con los requisitos de complejidad.
    **Argumentos:**
    password: La contraseña a validar.
    **Retorno:**
    True si la contraseña es compleja, False en caso contrario.
    """
    # Validar la longitud de la contraseña
    if len(password) < 8:
        return False

    # Validar que la contraseña contenga al menos un número
    if not any(char.isdigit() for char in password):
        return False

    # Validar que la contraseña contenga al menos una letra mayúscula
    if not any(char.isupper() for char in password):
        return False

    # Validar que la contraseña contenga al menos una letra minúscula
    if not any(char.islower() for char in password):
        return False

    # La contraseña cumple con todos los requisitos
    return True


def cambiar_contrasena(request):
  
  if request.method == 'POST':
    #form = PasswordChangeForm(user=request.user, data=request.POST)
    form = AuthenticationForm(request, data=request.POST)
    print(request.POST)
    if form.is_valid():
        password = form.cleaned_data.get('password')
        nueva_contrasena = form.cleaned_data.get('new_password1')
        confirmar_contrasena = form.cleaned_data.get('new_password2')
        username = form.cleaned_data.get('username')
        user = authenticate(username=username, password=password)
        print("Si es un metodo POST")
        print(request.POST)
        # Validar la contraseña actual
        if request.user.is_authenticated:
            if request.user.check_password(password):
                print("Se esta validando la pass actual" )
                messages.error(request, "La contraseña actual no es válida.")
                return redirect('index')

        # Validar que la nueva contraseña y la confirmacion coincidan
        if nueva_contrasena != confirmar_contrasena:
          print("Las contraseñas no coinciden")
          messages.error(request, "Las contraseñas no coinciden.")
          return redirect('index')
        
        
        # Validar la complejidad de la nueva contraseña
        #if not password_complex(password):
         # print("se valido la complejidad de la nueva contraseña")
          #messages.error(request, "La contraseña no cumple con los requisitos de seguridad.")
          #return redirect('index')
        
        # Validar que la nueva contraseña no sea igual a la actual
        if request.user.check_password(nueva_contrasena):
                messages.error(request, "La nueva contraseña no puede ser igual a la contraseña actual.")
        else:
              # Actualizar la contraseña del usuario
              request.user.set_password(nueva_contrasena)
              request.user.save()
              print("Se guardo la nueva contrasena")
              update_session_auth_hash(request, user)  # Importante para mantener la sesión activa.

        # Iniciar sesión al usuario con la nueva contraseña
        login(request, request.user)

        # Mostrar mensaje de éxito y redireccionar al cambio de contraseña
        messages.success(request, "Tu cuenta ha sido activada")
        # Mostrar mensaje de éxito y redireccionar al usuario al login
        messages.success(request, "Tu contraseña ha sido actualizada. Inicia sesión con tu nueva contraseña.")
        return redirect('login')
    else:
          messages.error(request, "Formulario no válido")
          print("Formulario no válido")
          print(form.errors)
          return redirect('index')
          
  # Si no es un método POST, mostrar el formulario de cambio de contraseña
  else:
    print("NO es un metodo POST")
    return redirect('login')
