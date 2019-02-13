from django.shortcuts import render
from django.contrib.auth import logout

# Create your views here.

def lout(request):
    logout(request)
    return render(request,'html/login.html')
