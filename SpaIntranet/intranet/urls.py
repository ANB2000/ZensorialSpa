from django.urls import path
from . import views
from .views import ActivateAccountView, CustomLoginView
urlpatterns = [

    path('', views.login_view, name='login'),
    path('home/', views.home_view, name='home'),
    path('ficha/', views.ficha_view, name='ficha'),
    path('activate_acount/', views.activate_view, name='activate_account'),

    path('activate-account/<int:user_id>/', ActivateAccountView.as_view(), name='activate_account'),
    
]
