from django.shortcuts import render

# Create your views here.

def notfound_404(request):
    return render(request,'html/404notfound.html')
def serverfailure(request):
    return render(request,'html/serverfailure.html')
