from django.shortcuts import render


def login(request):
    return render(request,'intranet/login.html')