from django.shortcuts import render
from django.http import HttpResponse
import json
from dashboard.models import Teacher
# Create your views here.
def index(request):
    teachers = Teacher.objects.all()
    data = {
        'teachers':teachers
    }
    return render(request,'html/home/index.html',data)

def register(request):
    return render(request,'html/home/Register.html')
