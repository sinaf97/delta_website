from django.shortcuts import render,redirect
from django.contrib.auth import logout

# Create your views here.

def lout(request):
    next = request.GET.get('next')
    logout(request)
    if next != '' or next != 'None' or next is not None:
        if 'dashboard' not in next:
            return redirect(next)
    return render(request,'html/login.html')
