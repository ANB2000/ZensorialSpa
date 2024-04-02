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
    path('cita/detalle_cita/<int:pk>/', views.detalle_cita, name='detalle_cita'),
    path('mostrar_cita//<int:pk>/', views.mostrar_cita_view, name='mostrar_cita'),
    path('verificar_disponibilidad/', views.verificar_disponibilidad, name='verificar_disponibilidad'),
    path('empleadoupdate/', views.empleadoupdate_view, name='empleadoupdate'),
    path('empleadonew/', views.empleadonew_view, name='empleadonew'),
    path('empleadodelete/', views.empleadodelete_view, name='empleadodelete'),
    path('crear_ficha_clinica/', views.crear_ficha_clinica, name='crear_ficha_clinica'),

]
