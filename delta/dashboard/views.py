from django.shortcuts import render
from .models import term , course,score,student
import json

# Create your views here.
# def getCurrentCourse(request):
#     t_courses = request.user.teacher.courses.all()
#     last_term = term.objects.last()
#     list = []
#     for i in t_courses:
#         if i.term == term.objects.last():
#             list.append(i.getCourseInfo())
#     return list

def courseConverter(info):
    info = info.split("_")
    info[1] = int(info[1])
    info[2] = int(info[2])
    info[4] = int(info[4])
    studentList = []
    theCourse = course.objects.all().filter(code=info[0],group=info[1])
    for i in theCourse:
        if(i.term.year == info[2] and i.term.season == info[3] and i.term.part == info[4]):
            theCourse = i
            break
    return theCourse

def orderKeyYear(e):
    return e['term']['year']
def orderKeySeason(e):
    if e['term']['season']=="spring":
        return 1
    elif e['term']['season']=="summer":
        return 2
    elif e['term']['season']=="fall":
        return 3
    elif e['term']['season']=="winter":
        return 4
def orderKeyPart(e):
    return e['term']['part']

def orderKeyYearTerm(e):
    return e['year']
def orderKeySeasonTerm(e):
    if e['season']=="spring":
        return 1
    elif e['season']=="summer":
        return 2
    elif e['season']=="fall":
        return 3
    elif e['season']=="winter":
        return 4
def orderKeyPartTerm(e):
    return e['part']

def getCourse(request):
    t_courses = request.user.teacher.courses.all()
    list = []
    for i in t_courses:
        list.append(i.getCourseInfo())
        sortCourses(list)
    return list

def sortCourses(list):
    list.sort(key=orderKeyPart,reverse=True)
    list.sort(key=orderKeySeason,reverse=True)
    list.sort(key=orderKeyYear,reverse=True)
    # return list
def sortTerms(list):
    list.sort(key=orderKeyPartTerm)
    list.sort(key=orderKeySeasonTerm)
    list.sort(key=orderKeyYearTerm)


def dashboard(request):
    context = {
        "user" : request.user
    }
    if request.user.username[0]=='s':
        return render(request,"html/dashboard/student/dashboard_s.html",context)
    elif request.user.username == "admin":
        return render (request,"html/dashboard/admin/dashboard_a.html",context)
    else:
        lastTerm = []
        for i in term.objects.all():
            lastTerm.append(i.getTermInfo())
        if lastTerm:
            sortTerms(lastTerm)
            lastTerm = lastTerm[-1]
        print(lastTerm)
        count = 0
        for i in request.user.teacher.courses.all():
            if i.term.getTermInfo() == lastTerm:
                count = count + len(i.students.all())
                print(i.students.all())
        context = {
        'count':count,
        'courses' : getCourse(request),
        'lastTerm':lastTerm
        }
        return render (request,"html/dashboard/teacher/dashboard_t.html",context)


def studentScore(request):
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
                sina["text"] =  j.course.term.season + " " + str(j.course.term.part)+":"+j.course.course_name +"******** Midterm: " + str(j.midScore) +" - Final: " + str(j.finalScore)
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
    context = getCourse(request)
    return render(request,'html/dashboard/teacher/courses.html',context)
def courseInfo(request,info):
    theCourse = courseConverter(info)
    lastTerm = []
    for i in term.objects.all():
        lastTerm.append(i.getTermInfo())
    sortTerms(lastTerm)
    lastTerm = lastTerm[-1]

    students = []
    for i in theCourse.students.all():
        students.append(i.getStudentInfo())
    scores = []
    for i in theCourse.scores.all():
        scores.append(i.getScoreInfo())
    context = {
    'lastTerm':lastTerm,
    'rawInfo': theCourse,
    'info':theCourse.getCourseInfo(),
    'courses': getCourse(request),
    'students':students,
    'scores':scores,
    }
    return render(request,'html/dashboard/teacher/course_info.html',context)

def commiteScore(request,theCourse,username,midscore,finalscore):
    if midscore=="":
        midscore = 0
    if finalscore=="":
        finalscore = 0
    std = student.objects.filter(user__username__contains=username).first()
    new = score(student=std,course=theCourse,midScore=midscore,finalScore=finalscore)
    exist = score.objects.filter(student=std,course=theCourse).first()
    if exist is None:
        new.save()
    else:
        score.objects.filter(student=std,course=theCourse).update(midScore=midscore,finalScore=finalscore)

def add_score(request):
    info = request.POST["course"]
    theCourse = courseConverter(info)
    students = theCourse.students.all()
    for i in students:
        midScore = request.POST[("midterm_"+i.user.username)]
        finalScore = request.POST[("final_"+i.user.username)]
        commiteScore(request,theCourse,i.user.username,midScore,finalScore)
    return render(request,'html/dashboard/teacher/submit.html')
