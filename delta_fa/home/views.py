from django.shortcuts import render,redirect
from django.http import HttpResponse
import json
from dashboard.models import Teacher
# Create your views here.
def index(request,lang = "fa"):
    teachers = Teacher.objects.all()
    data = {
    'teachers':teachers
    }
    return render(request,lang+'/html/home/index.html',data)

def register(request):
    return render(request,lang+'/html/home/Register.html')
def change_lang(request,lang):
    next = request.GET.get('next')
    if lang == "fa":
        lang = "en"
    else:
        lang = "fa"
    next = '/'+lang +next[3:]
    return redirect(next)
