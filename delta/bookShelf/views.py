from django.shortcuts import render
from .models import term , course,score,student,User,teacher,message
from .models import courseInfo as course_info
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
import json
from django.core import serializers
from .methods import *
from django.contrib.auth.decorators import login_required



class default:

    def main(request):
        pass
