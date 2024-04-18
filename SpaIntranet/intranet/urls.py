from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('home/', views.home_view, name='home'),
    path('ficha/', views.ficha_view, name='ficha'),
    path('change_pass/', views.activate_view, name='change_pass'),
    path('cita/', views.cita_view, name='cita'),
    path('cambio_contrasena_form/', views.pass_view, name='cambio_contrasena_form'),
    path('cambiar_contrasena/', views.cambiar_contrasena, name='cambiar_contrasena'),
    path('user_validate/', views.user_validate, name='user_validate'),
    path('crear_cita/', views.crear_cita, name='crear_cita'),
    path('mostrar_cita/<str:telefono_cliente>/', views.mostrar_cita_view, name='mostrar_cita'),
    path('verificar_disponibilidad/', views.verificar_disponibilidad, name='verificar_disponibilidad'),
    path('empleadoupdate/', views.empleadoupdate_view, name='empleadoupdate'),
    path('empleadonew/', views.empleadonew_view, name='empleadonew'),
    path('empleadodelete/', views.empleadodelete_view, name='empleadodelete'),
    path('crear_ficha_clinica/', views.crear_ficha_clinica, name='crear_ficha_clinica'),
    path('mostrar_ficha/<int:telefono_cliente>/', views.mostrar_ficha_view, name='mostrar_ficha'),
    path('alta_empleado/', views.alta_empleado, name='alta_empleado'),
    path('eliminar_empleado/', views.eliminar_empleado, name='eliminar_empleado'),
    path('actualizar_empleado/', views.actualizar_empleado, name='actualizar_empleado'),
    path('calendario/', views.calendario_view, name='calendario'),
    path('usuarios/', views.usuarios_view, name='usuarios'),
    path('buscar_cita/', views.buscar_cita_view, name='buscar_cita'),
    path('buscar_citas/', views.buscar_citas, name='buscar_citas'),
    path('busquedaficha/', views.buscar_ficha_view, name='busquedaficha'),
    path('buscarCita_eliminar/', views.buscarCita_eliminar_view, name='buscarCita_eliminar'),
    path('buscar_citasEliminar/', views.buscar_citasEliminar, name='buscar_citasEliminar'),
    path('mostrarEliminar_cita/<str:telefono_cliente>/', views.mostrarEliminar_cita_view, name='mostrarEliminar_cita'),
    path('eliminar_cita/<int:id>/', views.eliminar_cita, name='eliminar_cita')
    
]
