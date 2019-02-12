from django.shortcuts import render
from .models import term
import json

# Create your views here.

def dashboard(request):
    context = {
        "user" : request.user
    }
    if request.user.username[0]=='s':
        return render(request,"html/dashboard/student/dashboard_s.html",context)
    else:
        count = 0
        for i in request.user.teacher.courses.all():
            if i.term == term.objects.last():
                count = count + len(i.students.all())
        context['count'] = count
        return render (request,"html/dashboard/teacher/dashboard_t.html",context)


def score(request):
    scores = request.user.student.scores.all()
    # list = []
    # for i in scores:
        # list.append(i.course.term)
    dic = {}
    list2 = []
    sina = {}
    for i in range(1399,1395,-1):
        list2 = []
        for j in reversed(scores):
            if j.course.term.year == i:
                sina["text"] =  j.course.term.season + " " + str(j.course.term.part) +"******** score: " + str(j.scorenum)
                list2.append(sina)
                dic[str(i)] = list2
                sina = {}
    tree = []
    json1 = {}
    for key,value in dic.items():
        json1["text"] = key
        json1["selectable"]=0
        json1["state"]={"expanded":0}
        json1["nodes"] = value
        tree.append(json1)
        json1 = {}
    tree = json.dumps(tree)
    context = {
        "tree" : tree
    }
    return render (request,"html/dashboard/student/score.html",context)


def s_messege(request):
    return render(request,'html/dashboard/student/s_messege.html')

def r_messege(request):
    return render(request,'html/dashboard/student/r_messege.html')


def reports(request):
    return render(request,'html/dashboard/student/reports.html')

def courses(request):
    t_courses = request.user.teacher.courses.all()
    last_term = term.objects.last()
    list = []
    for i in t_courses:
        if i.term == term.objects.last():
            list.append(i)
    context = {
    "courses" : list,
    }
    return render(request,'html/dashboard/teacher/courses.html',context)
