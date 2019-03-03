from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
# Create your views here.


def lin(request):
    if not request.user.is_authenticated:
        return render(request,"html/Login.html",{"message":None})

    return HttpResponseRedirect(reverse('dashboard'))




def auth(request):
    delta_id = request.POST["delta_id"]
    password = request.POST["password"]
    user = authenticate(request,username=delta_id,password=password)
    if user is not None:
        login(request,user)
        return HttpResponseRedirect(reverse('lin'))
    return render(request,"html/Login.html",{"message":"Invalid Creditionals"})
