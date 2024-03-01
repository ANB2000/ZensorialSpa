from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.shortcuts import redirect

def login_view(request):
 return render(request,'intranet/login.html')

def home_view(request):
 return render(request,'intranet/home.html')

@login_required
@permission_required('app.permission_code', raise_exception=True)
def mi_vista(request):
    return # Código de la vista

class ActivateAccountView(FormView):
    template_name = 'intranet/activate_account.html'
    form_class = SetPasswordForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = User.objects.get(pk=self.kwargs['user_id'])
        return kwargs

    def form_valid(self, form):
        user = form.save()
        user.is_active = True
        user.save()
        login(self.request, user)
        return redirect(reverse_lazy('login.html'))
        
   # Con esta funcion te aseguras que el usuario pase forsosamente por el login 
    def dispatch(self, *args, **kwargs):
        user = User.objects.get(pk=self.kwargs['user_id'])
        if user.is_active:
            raise PermissionDenied("Este usuario ya está activo.")
        return super().dispatch(*args, **kwargs)

class CustomLoginView(LoginView):
    template_name = 'intranet/login.html'

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)

        if user is not None and not user.is_active:
            # Si el usuario existe pero está inactivo, redirigir al cambio de contraseña
            return redirect('activate_account.html', user_id=user.id)
        return super().form_valid(form)
