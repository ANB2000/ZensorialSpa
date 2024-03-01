from django.shortcuts import render
from django.shortcuts import redirect

def login_view(request):
 return render(request,'SpaIntranet/login.html')

def home_view(request):
 return render(request,'SpaIntranet/home.html')