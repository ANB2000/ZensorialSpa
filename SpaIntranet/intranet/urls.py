from django.urls import path
from . import views

urlpatterns = [

    path('', views.login_view, name='login'),
    path('home/', views.home_view, name='home'),
    path('ficha/', views.ficha_view, name='ficha'),
    path('index/', views.activate_view, name='index'),
    path('cita/', views.cita_view, name='cita'),
    path('cambio_contrasena_form/', views.pass_view, name='cambio_contrasena_form'),
    path('cambiar_contrasena/', views.cambiar_contrasena, name='cambiar_contrasena'),
    path('user_validate/', views.user_validate, name='user_validate'),
    

]
