from django.shortcuts import render
from django.http import HttpResponse
import json
# Create your views here.
def index(request):
    return render(request,'html/index.html')

def register(request):
    return render(request,'html/Register.html')
