from django.shortcuts import render


def login_view(request):
 return render(request,'SpaIntranet/login.html')

def home_view(request):
 return render(request,'SpaIntranet/home.html')

def ficha_view(request):
 return render(request,'SpaIntranet/ficha.html')