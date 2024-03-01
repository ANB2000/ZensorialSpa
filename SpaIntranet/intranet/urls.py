from django.urls import path
from .views import login
from .views import ActivateAccountView, CustomLoginView
urlpatterns = [

    path('', login, name='login'),
    path('activate-account/<int:user_id>/', ActivateAccountView.as_view(), name='activate_account'),
    path('login/', CustomLoginView.as_view(), name='login'),
    
    
]
