from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, authenticate, login
from .models import Cliente, Personal, Cita, FichaClinica
from django.utils.dateparse import parse_date, parse_time
from django.utils import timezone
from django.db.models import Q
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime



#Funcion para actualizar el status de los empleados
def actualizar_estado_personal():
    ahora = timezone.now()
    for empleado in Personal.objects.all():
        if empleado.horario_laboral_inicio <= ahora.time() <= empleado.horario_laboral_fin:
            nuevo_estado = 'disponible'
        else:
            nuevo_estado = 'no_disponible'
        if empleado.status != nuevo_estado:
            empleado.status = nuevo_estado
            empleado.save()


#Funcion para la validacion del usuario
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
            print("Formulario valido")
            user = authenticate(username=username, password=password)
            
            if user:
                print("Usuario autenticado")
                if user.is_active:
                    print("Usuario Activo y validado")
                    login(request, user)  # Iniciar sesión con el usuario autenticado
                    if password == 'ZensorialSpa2024*':
                        print("Contraseña por defecto reconocida, redirigiendo a cambiar contraseña")
                        messages.success(request, "Usuario existente, cambia tu contraseña")
                        return redirect('change_pass')  # Redirigir a la página de cambio de contraseña
                    else:
                        print("Usuario valido, ya cambio su contraseña")
                        messages.success(request, "Usuario y contraseña correctos.")
                        # Llamar a la función para actualizar el estado del personal
                        actualizar_estado_personal()
                        print("SE ACTUALIZO EL STATUS DE LOS EMPLEADOS")
                        # Reiniciar o establecer el flujo de la sesión
                        request.session['flow'] = 'home'
                        return redirect('home')  # Redirigir a la página de inicio después del login
                else:
                    print("El Usuario no esta activo")
                    messages.error(request, "Usuario Inactivo")
            else:
                print("Credenciales incorrectas")
                messages.error(request, "Información de inicio de sesión inválida.")
        else:
            print("Formulario no válido")
            print(form.errors)

    messages.error(request, "Información de inicio de sesión inválida.")
    return redirect('login')



# Vistas del cambio de contraseña
@login_required
def pass_view(request):
 return render(request,'intranet/cambio_contrasena_form.html')

@login_required
def activate_view(request):
    if 'change_pass' in request.session.get('flow', []):
        return render(request,'intranet/change_pass.html')

def login_view(request):
    # Comprobar si el flujo de la sesión está en 'home'
    if request.session.get('flow') == 'login':
        # Avanzar al siguiente paso del flujo
        request.session['flow'] = ['cambio_contrasena_form', 'change_pass']
        return render(request,'intranet/home.html')
    else:
        return render(request,'intranet/login.html')

@login_required
def home_view(request):
    # Comprobar si el flujo de la sesión está en 'home'
    if request.session.get('flow') == 'home':
        # Avanzar al siguiente paso del flujo
        request.session['flow'] = ['cita', 'ficha', 'change_pass', 'mostrar_cita']
        return render(request,'intranet/home.html')
    else:
        return redirect('login')
 
@login_required
def cita_view(request):
    if 'cita' in request.session.get('flow', []):
        # Obtener empleados disponibles
        print("Validando la disponibilidad de los empleados")
        empleados_disponibles = Personal.objects.filter(status='disponible')

        # Pasar los empleados disponibles al contexto del template
        context = {
            'empleados_disponibles': empleados_disponibles,
        }

        return render(request, 'intranet/cita.html', context)

    # Si 'cita' no está en el flujo, redirigir a otra página (por ejemplo, home)
    print("CITA NO ESTA DENTRO DEL FLOW, REDIRECT HOME")
    return redirect('home')

@login_required
def mostrar_cita_view(request, pk):
    if 'mostrar_cita' in request.session.get('flow', []):
        cita = get_object_or_404(Cita, pk=pk)
        messages.success(request, "ESTA ES LA INFORMACION QUE GUARDASTE PARA ESTA CITA")
        print("ENTRO A LA FUNCION PARA MOSTRAR LA CITA")
        return render(request, 'intranet/mostrar_cita.html', {'cita': cita})
        

@login_required
def ficha_view(request):
 return render(request,'intranet/ficha.html')

@login_required
def empleadoupdate_view(request):
    print("ENTRO A LA FUNCION DE VISTA PARA MODIFICAR AL EMPLEADO")
    return render(request,'intranet/empleadoupdate.html')

@login_required
def empleadonew_view(request):
    print("ENTRO A LA FUNCION DE VISTA PARA CREAR NUEVO EMPLEADO")
    return render(request,'intranet/empleadonew.html')

@login_required
def empleadodelete_view(request):
    print("ENTRO A LA FUNCION DE VISTA PARA ELIMINAR UN EMPLEADO")
    return render(request,'intranet/empleadodelete.html')

#Funcion para el cambio de contraseña
@login_required
def cambiar_contrasena(request):
    print("Entro a la Funcion cambiar contraseña")
    if 'change_pass' in request.session.get('flow', []):
        if request.method == 'POST':
            print("Si es un metodo POST")
            if request.user.is_authenticated:
                form = PasswordChangeForm(user=request.user, data=request.POST)
                if form.is_valid():

                    print("El formulario si es valido")
                    user = form.save()
                    print("Se guardo la nueva contrasena")
                    update_session_auth_hash(request, user)  # Importante para mantener la sesión activa.
                    messages.success(request, "Tu contraseña ha sido actualizada. Inicia sesión con tu nueva contraseña.")
                    return redirect('login')
                else:
                    messages.error(request, "Por favor, corrige los errores abajo.")
                    print(form.errors)
            else:
                messages.error(request, "No estás autenticado INTRUSO.")
                return redirect('login')
        else:
            print("No es un metodo POST, redirigiendo a change_pass")
            if request.user.is_authenticated:
                form = PasswordChangeForm(user=request.user)
                
                return render(request, 'change_pass.html', {'form': form})
            else:
                messages.error(request, "No estás autenticado.")
                return redirect('login')
    else: 
        return redirect('login')

@login_required
def detalle_cita(request, pk):
    cita = get_object_or_404(Cita, pk=pk)
    print("ENTRO A LA FUNCION PARA DIRECCIONAR A MOSTRAR_CITA")
    return render(request, 'intranet/mostrar_cita.html', {'cita': cita})
    

#FUNCION PARA VERIFICAR LA DISPONIBILIDAD DE LOS EMPLEADOS
@csrf_exempt
@require_POST
def verificar_disponibilidad(request):
    data = json.loads(request.body)
    hora_inicio_str = data.get('horaInicio')
    fecha_cita_str = data.get('fechaCita')

    if not hora_inicio_str or not fecha_cita_str:
        return JsonResponse({'error': 'Falta hora de inicio o fecha de la cita'}, status=400)

    # Parsear la hora y fecha de la cadena de texto a objetos de Python
    try:
        hora_inicio_nueva_cita = datetime.strptime(hora_inicio_str, '%H:%M').time()
        fecha_nueva_cita = datetime.strptime(fecha_cita_str, '%Y-%m-%d').date()
    except ValueError as e:
        return JsonResponse({'error': 'Formato de fecha u hora inválido'}, status=400)

    # Filtrar empleados disponibles dentro de su horario laboral
    empleados_disponibles = Personal.objects.filter(status='disponible')

    empleados_finales = []
    for empleado in empleados_disponibles:
        # Verificar si el empleado tiene citas en la misma fecha de la nueva cita
        citas_existentes_mismo_dia = Cita.objects.filter(
            asignado_a=empleado,
            fecha_cita__date=fecha_nueva_cita
        )

        # Verificar si la hora de la nueva cita choca o está dentro del horario de alguna de las citas existentes
        choque = citas_existentes_mismo_dia.filter(
            Q(horario_cita_inicio__lt=hora_inicio_nueva_cita, horario_cita_fin__gt=hora_inicio_nueva_cita) |
            Q(horario_cita_inicio__lte=hora_inicio_nueva_cita, horario_cita_fin__gte=hora_inicio_nueva_cita)
        ).exists()

        # Si no hay choque, el empleado está disponible
        if not choque:
            empleados_finales.append(empleado)
        else:
            messages.error(request, "NO HAY EMPLEADOS DISPONIBLES PARA ATENDER ESTA CITA")

    # Crear la lista de empleados para la respuesta
    empleados_data = [{'id': empleado.id, 'nombre': empleado.nombre_empleado} for empleado in empleados_finales]

    return JsonResponse({'empleados': empleados_data})

#Funcion para crear una cita
@login_required
def crear_cita(request):
    if 'cita' in request.session.get('flow', []):

        if request.method == 'POST':
            fecha_cita_str = request.POST.get('fechaCita')
            fecha_cita = datetime.strptime(fecha_cita_str, '%Y-%m-%d').date() if fecha_cita_str else None
            status = request.POST.get('statusCita', 'por_confirmar')
            paquete = request.POST.get('paqueteCita', 'No')
            nombre_cliente = request.POST.get('nombreCliente')
            telefono_cliente = request.POST.get('telefonoCliente')
            servicio = request.POST.get('servicio')
            total_sesiones_input = request.POST.get('totalSesiones', '0')
            total_sesiones = int(total_sesiones_input) if total_sesiones_input.isdigit() else 0
            sesiones_tomadas_input = request.POST.get('sesionesTomadas', '0')
            sesiones_tomadas = int(sesiones_tomadas_input) if sesiones_tomadas_input.isdigit() else 0
            metodo_pago = request.POST.get('metodoPago')
            horario_cita_inicio_str = request.POST.get('horaInicio')
            horario_cita_fin_str = request.POST.get('horaFin')
            horario_cita_inicio = parse_time(horario_cita_inicio_str) if horario_cita_inicio_str else None
            horario_cita_fin = parse_time(horario_cita_fin_str) if horario_cita_fin_str else None
            observaciones = request.POST.get('observaciones', '')[:255]
            asignado_a_id = request.POST.get('asignado')  # Asume que 'asignado' es el ID del empleado
            print(request.POST)

            cliente, created = Cliente.objects.get_or_create(
                telefono_cliente=telefono_cliente,
                defaults={'nombre_cliente': nombre_cliente}
            )
            if created:
                messages.success(request, "Nuevo cliente creado con éxito.")
            else:
                messages.success(request, "ESTE CLIENTE YA TIENE ALGUN REGISTRO")
                
            asignado_a = get_object_or_404(Personal, pk=asignado_a_id)
            
            sesiones_faltantes = total_sesiones - sesiones_tomadas

            cita = Cita.objects.create(
                nombre_cliente=cliente,
                fecha_cita=fecha_cita,
                horario_cita_inicio=horario_cita_inicio,
                horario_cita_fin=horario_cita_fin,
                servicio=servicio,
                metodo_pago=metodo_pago,
                paquete=paquete,
                total_sesiones=total_sesiones,
                sesiones_tomadas=sesiones_tomadas,
                sesiones_faltantes=sesiones_faltantes,
                observaciones=observaciones,
                status=status,
                asignado_a=asignado_a
            )

            messages.success(request, "CITA CREADA CON EXITO")
            print("Mostrando cita")
            return redirect('mostrar_cita', pk=cita.pk)

        else:
            return render(request, 'cita.html')

    else:
        messages.error(request, "NO PUEDES SALTARTE LAS VISTAS")
        return redirect('home')

#Funcion para crear una FICHA CLINICA
@login_required
def crear_ficha_clinica(request):
    if request.method == 'POST':
        # Aquí capturas los datos del formulario
        fecha_ficha = request.POST.get('fecha')
        nombre_cliente = request.POST.get('nombrePaciente')
        telefono = request.POST.get('telefono')
        edad = request.POST.get('edad')
        genero = request.POST.get('genero')
        estado_civil = request.POST.get('estadoCivil')
        ocupacion = request.POST.get('ocupacion')
        motivo_consulta = request.POST.get('motivoConsulta')
        cardiovasculares = request.POST.get('motivoConsulta')
        pulmonares = request.POST.get('motivoConsulta')
        digestivos = request.POST.get('motivoConsulta')
        otros = request.POST.get('motivoConsulta')
        sexo = request.POST.get('motivoConsulta')
        renales = request.POST.get('motivoConsulta')
        alergicos = request.POST.get('motivoConsulta')
        quirurgicos = request.POST.get('motivoConsulta')
        respiratorios = request.POST.get('motivoConsulta')
        alcoholismo = request.POST.get('motivoConsulta')
        tabaquismo = request.POST.get('motivoConsulta')
        drogas = request.POST.get('motivoConsulta')
        otro = request.POST.get('motivoConsulta')
        madre = request.POST.get('motivoConsulta')
        enfermed_madre = request.POST.get('motivoConsulta')
        padre = request.POST.get('motivoConsulta')
        enfermed_padre = request.POST.get('motivoConsulta')
        inicio_menstruacion = request.POST.get('motivoConsulta')
        ciclo_menstruacion = request.POST.get('motivoConsulta')
        duracion_menstruacion = request.POST.get('motivoConsulta')
        ultima_regla = request.POST.get('motivoConsulta')
        anticonceptivos = request.POST.get('motivoConsulta')
        menopausia = request.POST.get('motivoConsulta')
        peso = request.POST.get('motivoConsulta')
        talla = request.POST.get('motivoConsulta')
        imc = request.POST.get('motivoConsulta')
        

        # Supongamos que ya tienes un cliente creado, lo buscas o lo creas
        cliente, created = Cliente.objects.get_or_create(
            nombre=nombrePaciente, 
            defaults={'telefono': telefono}
        )

        # Creas la ficha clínica
        ficha_clinica = FichaClinica.objects.create(
            nombre_cliente=cliente,
            fecha_ficha=timezone.now() if not fecha else timezone.datetime.strptime(fecha, '%Y-%m-%d'),
            edad=edad,
            ocupacion=ocupacion,
            motivo_consulta=motivoConsulta[:30],  # Ejemplo de limitación de longitud
            sexo=genero,
            estado_civil=estadoCivil
            # Agrega los demás campos según tu modelo
        )

        messages.success(request, "Ficha clínica creada con éxito")
        return redirect('alguna_url_de_confirmacion')
    else:
        # Si es un GET, solo renderizas el formulario
        return render(request, 'tu_template_de_ficha_clinica.html')

@login_required    
  #Funcion para buscar citas  
def buscar_citas_por_telefono(request):
    if request.method == 'POST':
        telefono_cliente = request.POST.get('telefonoCita')
        cliente = Cliente.objects.filter(telefono=telefono_cliente).first()

        if cliente:
            citas = Cita.objects.filter(cliente=cliente)
            return render(request, 'lista_citas.html', {'citas': citas, 'cliente': cliente})
        else:
            messages.error(request, "No se encontraron citas para el número proporcionado.")
            return redirect('buscar_citas_por_telefono')

    return render(request, 'buscar_citas.html')
#esto va en el html para buscar cita
#<form method="post">
 #   {% csrf_token %}
  #  <label for="telefonoCita">Número de teléfono:</label>
   # <input type="text" id="telefonoCita" name="telefonoCita">
    #<button type="submit">Buscar Citas</button>
#</form>

#funcion para editar informacion de la cita
@login_required
def editar_cita(request, cita_id):
    cita = Cita.objects.get(id=cita_id)

    if request.method == 'POST':
        # Aquí procesas el formulario de edición de la cita
        # Puedes usar un formulario de Django para facilitar la validación y actualización
        return redirect('detalle_cita', pk=cita.id)

    return render(request, 'editar_cita.html', {'cita': cita})