from django.urls import path
from . import views
from .views import ActivateAccountView, CustomLoginView
urlpatterns = [

    path('', views.login_view, name='login'),
    path('home/', views.home_view, name='home'),
    path('activate-account/<int:user_id>/', ActivateAccountView.as_view(), name='activate_account'),
    
]
