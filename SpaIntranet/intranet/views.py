from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, authenticate, login
from .models import Cliente, Personal, Cita, FichaClinica
from django.utils.dateparse import parse_time
from django.utils import timezone
from django.db.models import Q
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.urls import reverse



#Funcion para actualizar el status de los empleados
def actualizar_estado_personal():
    ahora = timezone.localtime(timezone.now())
    print("Hora actual:", ahora.time())  # Depuración
    empleado = Personal.objects.all()
    for empleado in Personal.objects.all():
        inicio = empleado.horario_laboral_inicio
        fin = empleado.horario_laboral_fin
        nuevo_estado = 'disponible' if inicio <= ahora.time() <= fin else 'no_disponible'

        # Depuración
        print(f"Revisando empleado {empleado.nombre_empleado} ({inicio} - {fin}): {nuevo_estado}")

        if empleado.status != nuevo_estado:
           empleado.status = nuevo_estado
           empleado.save()
           print(f"Estado actualizado para {empleado.nombre_empleado} a {nuevo_estado}")
        else:
           print(f"No se requiere actualización para {empleado.nombre_empleado}")
        

#Funcion para la validacion del usuario
def user_validate(request):
    ahora = timezone.localtime()  # Asegúrate de usar la hora local correcta
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
                        messages.success(request, "BIENVENIDO, USUARIO Y CONTRASEÑA CORRECTOS, ")
                        # Llamar a la función para actualizar el estado del personal
                        actualizar_estado_personal()
                        print("SE ACTUALIZO EL STATUS DE LOS EMPLEADOS")
                        messages.info(request, "SE ACTUALIZO EL STATUS DE LOS EMPLEADOS.")
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
    if 'home' in request.session.get('flow', []):
        # Avanzar al siguiente paso del flujo
        request.session['flow'] = ['cita', 'ficha', 'change_pass', 'lista_citas','buscar_cita', 'buscarFicha',
                                   'buscar_citas','mostrar_cita', 'mostrar_ficha', 'crear_ficha','crear_cita', 'buscarCita_eliminar',
                                   'buscarFichaEliminar','mostrarFichaEliminar']
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
def buscar_cita_view(request ):
    if 'buscar_cita' in request.session.get('flow', []):
        return render(request,'intranet/buscar_cita.html')
    
@login_required
def buscarCita_eliminar_view(request ):
    if 'buscarCita_eliminar' in request.session.get('flow', []):
        return render(request,'intranet/buscarCita_eliminar.html')

@login_required
def buscarFichaEliminar_view(request ):
    if 'buscarFichaEliminar' in request.session.get('flow', []):
        request.session['flow'] = ['buscar_cita','home','ficha','buscarFichaEliminar','mostrarEliminar_cita']
        return render(request,'intranet/buscarFichaEliminar.html')

@login_required
def buscar_ficha_view(request ):
    if 'buscarFicha' in request.session.get('flow', []):
        return render(request,'intranet/buscarFicha.html')
    
def mostrarEliminar_cita_view(request ,telefono_cliente):
    if 'mostrarEliminar_cita' in request.session.get('flow', []):
        cliente = get_object_or_404(Cliente, telefono_cliente=telefono_cliente)
        citas = Cita.objects.filter(nombre_cliente=cliente)
        if citas.exists():
            messages.info(request, f"AHORA PUEDES ELIMINAR LAS CITAS EXISTENTES PARA EL CLIENTE CON EL NUMERO {telefono_cliente}.")
            return render(request, 'intranet/mostrarEliminar_cita.html', {'citas': citas, 'cliente': cliente})
        else:
            messages.error(request, "No se encontraron citas para el número proporcionado.")
            return redirect('buscar_cita')

def mostrar_cita_view(request ,telefono_cliente):
    if 'mostrar_cita' in request.session.get('flow', []):
        cliente = get_object_or_404(Cliente, telefono_cliente=telefono_cliente)
        citas = Cita.objects.filter(nombre_cliente=cliente)
        if citas.exists():
            messages.info(request, f"ESTAS SON LAS CITAS EXISTENTES PARA EL CLIENTE CON EL NUMERO {telefono_cliente}.")
            return render(request, 'intranet/mostrar_cita.html', {'citas': citas, 'cliente': cliente})
        else:
            messages.error(request, "No se encontraron citas para el número proporcionado.")
            return redirect('buscar_cita')
    

def mostrar_ficha_view(request, telefono_cliente):
    if 'mostrar_ficha' in request.session.get('flow', []):
        cliente = get_object_or_404(Cliente, telefono_cliente= telefono_cliente)
        fichas = FichaClinica.objects.filter(nombre_cliente=cliente)
        messages.info(request, "ESTA ES LA INFORMACION QUE GUARDASTE PARA ESTA FICHA CLINICA")
        print("ENTRO A LA FUNCION PARA MOSTRAR LA FICHA  CLINICA")
        print("Fichas encontradas:", fichas.count())
        request.session['flow'] = ['buscar_cita','home','ficha']
        return render(request, 'intranet/mostrar_ficha.html', {'fichas': fichas, 'cliente': cliente})
    else:
        messages.error(request, "No tienes acceso a esta página.")
        return redirect('home')

def mostrarFichaEliminar_view(request ,telefono_cliente):
    if 'mostrarFichaEliminar' in request.session.get('flow', []):
        cliente = get_object_or_404(Cliente, telefono_cliente=telefono_cliente)
        fichas = FichaClinica.objects.filter(nombre_cliente=cliente)
        if fichas.exists():
            messages.info(request, f"AHORA PUEDES ELIMINAR LAS FICHAS CLINICAS EXISTENTES PARA EL CLIENTE CON EL NUMERO {telefono_cliente}.")
            request.session['flow'] = ['buscar_cita','home','ficha']
            return render(request, 'intranet/mostrarFichaEliminar.html', {'fichas': fichas, 'cliente': cliente})
        else:
            messages.error(request, "No se encontraron fichas para el número proporcionado.")
            return redirect('buscarFichaEliminar')
    else:
        messages.error(request, "NO TIENES ACCESO A ESTA PAGINA.")
        return redirect('home')

@login_required
def usuarios_view(request):
 return render(request,'intranet/usuarios.html')

        
@login_required
def calendario_view(request):
 return render(request,'intranet/calendario.html')

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
                messages.success(request, "NUEVO CLIENTE REGISTRADO,")
            else:
                messages.info(request, "NO SE GUARDO EL CLIENTE O YA TIENE ALGUN REGISTRO CON NOSOTROS")
                
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

            messages.success(request, "NUEVA CITA CREADA CON EXITO.")
            request.session['flow'] = ['home' ,'mostrar_cita']
            print("Mostrando cita")
            return redirect('home')

        else:
            return render(request, 'cita')

    else:
        messages.error(request, "NO PUEDES SALTARTE LAS VISTAS")
        return redirect('home')

#Funcion para crear una FICHA CLINICA
@login_required
def crear_ficha_clinica(request):
    if request.method == 'POST':
        fecha_ficha_str = request.POST.get('fecha_ficha')
        fecha_ficha = datetime.strptime(fecha_ficha_str, '%Y-%m-%d').date() if fecha_ficha_str else None
        telefono_cliente= request.POST.get('telefono_cliente')
        edad = request.POST.get('edad')
        estado_civil = request.POST.get('estado_civil')
        ocupacion = request.POST.get('ocupacion')
        motivo_consulta = request.POST.get('motivo_consulta')
        cardiovasculares = request.POST.get('cardiovasculares')
        pulmonares = request.POST.get('pulmonares')
        digestivos = request.POST.get('digestivos')
        otros = request.POST.get('otros')
        sexo = request.POST.get('sexo')
        renales = request.POST.get('renales')
        alergicos = request.POST.get('alergicos')
        quirurgicos = request.POST.get('quirurgicos')
        respiratorios = request.POST.get('respiratorios')
        alcoholismo = request.POST.get('alcoholismo')
        tabaquismo = request.POST.get('tabaquismo')
        drogas = request.POST.get('drogas')
        otro = request.POST.get('otro')
        madre = request.POST.get('madre')
        enfermed_madre = request.POST.get('enfermed_madre')
        padre = request.POST.get('padre')
        enfermed_padre = request.POST.get('enfermed_padre')
        inicio_menstruacion_srt = request.POST.get('inicio_menstruacion')
        inicio_menstruacion = int(inicio_menstruacion_srt) if inicio_menstruacion_srt.isdigit() else None
        ciclo_menstruacion_str = request.POST.get('ciclo_menstruacion')
        ciclo_menstruacion = int(ciclo_menstruacion_str) if ciclo_menstruacion_str.isdigit() else None
        duracion_menstruacion_str = request.POST.get('duracion_menstruacion')
        duracion_menstruacion = int(duracion_menstruacion_str) if duracion_menstruacion_str.isdigit() else None
        ultima_regla_str = request.POST.get('fechaCita')
        ultima_regla = datetime.strptime(ultima_regla_str, '%Y-%m-%d').date() if ultima_regla_str else None
        anticonceptivos = request.POST.get('anticonceptivos')
        menopausia = request.POST.get('menopausia')
        peso_srt = request.POST.get('peso')
        peso = int(peso_srt) if peso_srt.isdigit() else None
        talla_srt = request.POST.get('talla')
        talla = int(talla_srt) if talla_srt.isdigit() else None
        imc_srt = request.POST.get('imc')
        imc = int(imc_srt) if imc_srt.isdigit() else None
        

        # Supongamos que ya tienes un cliente creado, lo buscas o lo creas
        cliente, created = Cliente.objects.get_or_create(
                telefono_cliente=telefono_cliente,
                defaults={'nombre_cliente': request.POST.get('nombre_cliente')}
        )
        if created:
                messages.success(request, "NUEVO CLIENTE REGISTRADO,")
        else:
                messages.info(request, "NO SE GUARDO EL CLIENTE O YA TIENE ALGUN REGISTRO CON NOSOTROS")
                
        
        # Creas la ficha clínica
        fichaClinica = FichaClinica.objects.create(
            fecha_ficha = fecha_ficha,
            nombre_cliente = cliente,
            edad = edad,
            estado_civil = estado_civil,
            ocupacion = ocupacion,
            motivo_consulta = motivo_consulta,
            cardiovasculares = cardiovasculares,
            pulmonares = pulmonares,
            digestivos = digestivos,
            otros = otros,
            sexo = sexo,
            renales = renales,
            alergicos = alergicos,
            quirurgicos = quirurgicos,
            respiratorios = respiratorios,
            alcoholismo = alcoholismo,
            tabaquismo = tabaquismo,
            drogas = drogas,
            otro = otro,
            madre = madre,
            enfermed_madre = enfermed_madre,
            padre = padre,
            enfermed_padre = enfermed_padre,
            inicio_menstruacion = inicio_menstruacion,
            ciclo_menstruacion = ciclo_menstruacion,
            duracion_menstruacion = duracion_menstruacion,
            ultima_regla = ultima_regla,
            anticonceptivos = anticonceptivos,
            menopausia = menopausia,
            peso = peso,
            talla = talla,
            imc = imc
        )
        request.session['flow'] = ['home' ,'mostrar_cita']
        messages.success(request, "FICHA CLINICA CREADA CON EXITO")
        print("FICHA CLINICA CREADA CON EXITO")
        print("Mostrando cita")
        return redirect('home')
        
    else:
        messages.error(request, f"Error al crear la ficha clínica")
        
        # Si es un GET, solo renderizas el formulario
        return render(request, 'ficha.html')


def alta_empleado(request):
    if request.method == 'POST':
        nombre_empleado = request.POST.get('nombre_empleado')
        status = request.POST.get('status')
        horario_inicio = request.POST.get('horario_laboral_inicio')
        horario_fin = request.POST.get('horario_laboral_fin')
        print(request.POST)
        
        # Crear y guardar el nuevo empleado en la base de datos
        empleado = Personal.objects.create(
            nombre_empleado=nombre_empleado,
            status=status,
            horario_laboral_inicio=horario_inicio,
            horario_laboral_fin=horario_fin
        )
        request.session['flow'] = ['home']
        messages.success(request, 'EMPLEADO CREADO EXITOSAMENTE.')
        return redirect(reverse('home'))  # Reemplaza 'home' con el nombre de tu URL de destino después de la creación.
    else:
        return render(request, 'intranet/empleadonew.html')  # Asegúrate de usar la plantilla correcta.


def eliminar_empleado(request):
    # Asegúrate de que estás procesando un POST
    if request.method == 'POST':
        nombre_empleado = request.POST.get('employeeId')
        
        # Intenta obtener el empleado y eliminarlo
        try:
            empleado = Personal.objects.get(nombre_empleado=nombre_empleado)
            empleado.delete()
            messages.success(request, f'El empleado {nombre_empleado} ha sido eliminado con éxito.')
        except Personal.DoesNotExist:
            messages.error(request, 'Empleado no encontrado.')
        except Exception as e:
            messages.error(request, f'Error al eliminar al empleado: {e}')
        
        # Redirige a la página deseada después de la operación
        request.session['flow'] = ['home']
        return redirect('home')
    else:
        # Si la solicitud no es POST, envía al usuario de vuelta al formulario
        return render(request, 'empleadodelete.html')

@login_required
def actualizar_empleado(request):
    empleado = None

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'buscar':
            nombre_busqueda = request.POST.get('empleadoupdate')
            empleado = get_object_or_404(Personal, nombre_empleado=nombre_busqueda)
            messages.info(request, f"MOSTRANDO DATOS PARA: {empleado.nombre_empleado}. PUEDES ACTUALIZAR SU INFORMACION.")
        
        elif action == 'actualizar':
            nombre_empleado = request.POST.get('nombre_empleado')
            empleado = get_object_or_404(Personal, nombre_empleado=nombre_empleado)
            empleado.horario_laboral_inicio = request.POST.get('horario_laboral_inicio')
            empleado.horario_laboral_fin = request.POST.get('horario_laboral_fin')
            empleado.save()
            messages.success(request, "INFORMACION DEL EMPLEADO ACTUALIZADA CON EXITO")
           # Redirige a la página deseada después de la operación
            request.session['flow'] = ['home']
            return redirect('home')
    context = {
        'empleado': empleado
    }
    return render(request, 'intranet/empleadoupdate.html', context)

  #Funcion para buscar citas  


def buscar_citas(request):
    if request.method == 'POST':
        telefono_cliente = request.POST.get('telefonoCita')
        cliente = Cliente.objects.filter(telefono_cliente=telefono_cliente).first()

        if cliente:
            cita = Cita.objects.filter(nombre_cliente=cliente)
            request.session['flow'] = ['mostrar_cita']
            return redirect('mostrar_cita', telefono_cliente=telefono_cliente)
        else:
            messages.error(request, "No se encontraron citas para el número proporcionado.")
            request.session['flow'] = ['buscar_cita']
            return redirect('buscar_cita')

    return render(request, 'buscar_cita.html')

def buscar_citasEliminar(request): 
    
    if request.method == 'POST':
        telefono_cliente = request.POST.get('telefonoCita')
        cliente = Cliente.objects.filter(telefono_cliente=telefono_cliente).first()

        if cliente:
            cita = Cita.objects.filter(nombre_cliente=cliente)
            request.session['flow'] = ['mostrarEliminar_cita']
            return redirect('mostrarEliminar_cita', telefono_cliente=telefono_cliente)
        else:
            messages.error(request, "No se encontraron citas para el número proporcionado.")
            request.session['flow'] = ['buscarCita_eliminar','home']
            return redirect('buscarCita_eliminar')

    return render(request, 'buscarCita_eliminar.html')

def eliminar_cita(request, id):
    if request.method == 'POST':
        cita = get_object_or_404(Cita, pk=id)
        cita.delete()
        messages.success(request, "CITA ELIMINADA CORRECTAMENTE.")
        request.session['flow'] = ['home']
        return redirect('home')  # Redirige a la página que desees después de eliminar
    else:
        messages.error(request, "NO SE PUDO ELIMINAR LA CITA.")
        return redirect('home')
    
    
def buscar_fichas(request):
    if request.method == 'POST':
        telefono_cliente = request.POST.get('telefonoFicha')
        cliente = Cliente.objects.filter(telefono_cliente=telefono_cliente).first()

        if cliente:
            ficha = FichaClinica.objects.filter(nombre_cliente=cliente)
            request.session['flow'] = ['mostrar_ficha']
            return redirect('mostrar_ficha', telefono_cliente=telefono_cliente)
        else:
            messages.error(request, "No se encontraron fichas para el número proporcionado.")
            request.session['flow'] = ['buscarFicha', 'home']
            return redirect('buscarFicha')

    return render(request, 'buscarFicha.html')

def buscarFichasEliminar(request): 
    
    if request.method == 'POST':
        telefono_cliente = request.POST.get('telefonoFicha')
        cliente = Cliente.objects.filter(telefono_cliente=telefono_cliente).first()

        if cliente:
            ficha = FichaClinica.objects.filter(nombre_cliente=cliente)
            request.session['flow'] = ['mostrarFichaEliminar']
            return redirect('mostrarFichaEliminar', telefono_cliente=telefono_cliente)
        else:
            messages.error(request, "No se encontraron fichas para el número proporcionado.")
            request.session['flow'] = ['buscarFichaElimina', 'home']
            return redirect('buscarFichaEliminar')
    request.session['flow'] = ['buscarFichaEliminar']
    return render(request, 'buscarFichaEliminar.html')

def eliminarFicha(request, id):
    if request.method == 'POST':
        ficha = get_object_or_404(FichaClinica, pk=id)
        ficha.delete()
        messages.success(request, "FICHA CLINICA ELIMINADA CORRECTAMENTE.")
        request.session['flow'] = ['home']
        return redirect('home')  # Redirige a la página que desees después de eliminar
    else:
        messages.error(request, "NO SE PUDO ELIMINAR LA CITA.")
        return redirect('home')