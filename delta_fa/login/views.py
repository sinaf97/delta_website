from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
# Create your views here.


def lin(request,lang="fa"):
    next = '/' + lang + '/dashboard'
    try:
        next = request.GET.get('next')
    except Exception as e:
        pass
    if not request.user.is_authenticated:
        return render(request,lang+"/html/Login.html",{"message":None,'next':next})
    return redirect('dashboard')




def auth(request,lang="fa"):
    delta_id = request.POST["delta_id"]
    password = request.POST["password"]
    next = request.POST['next']
    print(next)
    if(next == 'None' or next == '/' or next is None or next == ''):
        next = '/'+lang+'/dashboard'
    user = authenticate(request,username=delta_id,password=password)
    if user is not None:
        login(request,user)
        return redirect(next)
    return render(request,lang+"/html/Login.html",{"message":"Invalid Creditionals",'next':next})
