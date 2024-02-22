from django.urls import path
from intranet.views import login

urlpatterns = [
    path('', login, name='login'),# Esto hace que tome el login como la primer pagina al ejecutar la web
    
]