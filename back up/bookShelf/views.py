from django.shortcuts import render
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
import json
from django.core import serializers
from django.contrib.auth.decorators import login_required
from .models import *



class default:

    def main(request):
        book_groups = BookGroup.objects.all()
        context = {
            'groups':book_groups
        }
        return render(request,'html/books/index.html',context)
