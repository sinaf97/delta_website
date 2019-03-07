from django.shortcuts import render
from .models import term , course,score,student,User,teacher
from .models import courseInfo as course_info
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
import json
from django.core import serializers
from .methods import *
from django.contrib.auth.decorators import login_required



class default:
    # @login_required(login_url='/login')
    def dashboard(request):
            context = {
                "user" : request.user,
            }
            if request.user.role=="Student":
                context['info'] = {
                'term':term.objects.last(),
                'course':request.user.student.course.filter(term = term.objects.last()).first(),
                'score': request.user.student.scores.filter(course = request.user.student.course.filter(term = term.objects.last()).first()).first()
                }
                return render(request,"html/dashboard/student/dashboard_s.html",context)
            elif request.user.role=="Teacher":
                lastTerm = []
                for i in term.objects.all():
                    lastTerm.append(i.getTermInfo())
                if lastTerm:
                    sortTerms(lastTerm)
                    lastTerm = lastTerm[-1]
                count = 0
                for i in request.user.teacher.courses.all():
                    if i.term.getTermInfo() == lastTerm:
                        count = count + len(i.students.all())
                context = {
                'count':count,
                'courses' : getCourse(request),
                'lastTerm':lastTerm
                }
                return render (request,"html/dashboard/teacher/dashboard_t.html",context)
            else:
                return render (request,"html/dashboard/admin/dashboard_a.html",context)
    # @login_required(login_url='/login')
    def settings(request):
            if request.user.role == "Teacher":
                context = {
                'courses' : getCourse(request),
                }
                return render(request,"html/dashboard/teacher/settings.html",context)
            elif request.user.role == "Student":
                return render(request,"html/dashboard/student/settings.html")
            else:
                return render(request,"html/dashboard/admin/settings.html")
    # @login_required(login_url='/login')
    def change_name(request):
            request.user.first_name = request.POST["firstName"]
            request.user.last_name = request.POST["lastName"]
            request.user.save()
            context = {
                'new_name':request.user.get_full_name(),
                'msg':"Name changed successfully"
            }
            return JsonResponse(context)
    # @login_required(login_url='/login')
    def change_pass(request):
        if request.user.check_password(request.POST["oldpass"]):
            user = request.user
            user.set_password(request.POST["newpass"])
            user.save()
            update_session_auth_hash(request,user)
            msg = "Password changed successfully"
        else:
            msg = "Wrong old password"
        context = {
            'msg': msg
            }
        return JsonResponse(context)

class studentViews:
    # @login_required(login_url='/login')
    def studentScore(request):
            scores = request.user.student.scores.all()
            dic = {}
            list2 = []
            sina = {}
            for i in range(1399,1395,-1):
                list2 = []
                for j in reversed(scores):
                    if j.course.term.year == i:
                        sina["text"] = j.course.term.season + " " + str(j.course.term.part)+":"+j.course.courseInfo.course_name +"******** Midterm: " + str(j.midScore) +" - Final: " + str(j.finalScore)
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
            if 'admin' not in request.content_params.keys():
                return render (request,"html/dashboard/student/score.html",context)
            return context
    # @login_required(login_url='/login')
    def s_messege(request):
            return render(request,'html/dashboard/student/s_messege.html')
    # @login_required(login_url='/login')
    def r_messege(request):
            return render(request,'html/dashboard/student/r_messege.html')
    # @login_required(login_url='/login')
    def reports(request):
            return render(request,'html/dashboard/student/reports.html')
    # @login_required(login_url='/login')
    def info(request):
        data = {
            'user':request.user
        }
        return render (request,"html/dashboard/student/info.html",data)

class teacherViews:
    # @login_required(login_url='/login')
    def courses(request):
            context = getCourse(request)
            return render(request,'html/dashboard/teacher/courses.html',context)
    # @login_required(login_url='/login')
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
            return render(request,'html/dashboard/teacher/courseInfo.html',context)
    # @login_required(login_url='/login')
    def add_score(request):
            info = request.POST["course"]
            theCourse = courseConverter(info)
            students = theCourse.students.all()
            for i in students:
                midScore = request.POST[("midterm_"+i.user.username)]
                finalScore = request.POST[("final_"+i.user.username)]
                commiteScore(request,theCourse,i.user.username,midScore,finalScore)
            data = {
                'msg':"Scores submitted successfully"
            }
            return JsonResponse(data)
    # @login_required(login_url='/login')
    def commiteScore(request,theCourse,username,midscore,finalscore):
            if midscore=="":
                midscore = 0
            if finalscore=="":
                finalscore = 0
            std = student.objects.filter(user__username=username).first()
            new = score(student=std,course=theCourse,midScore=midscore,finalScore=finalscore)
            exist = score.objects.filter(student=std,course=theCourse).first()
            if exist is None:
                new.save()
            else:
                score.objects.filter(student=std,course=theCourse).update(midScore=midscore,finalScore=finalscore)
    # @login_required(login_url='/login')
    def info(request):
            data = {
                'user':request.user,
                'courses':getCourse(request)
            }
            return render (request,"html/dashboard/teacher/info.html",data)

class adminViews:
    # @login_required(login_url='/login')
    def add_user(request):
            context = {
                'status':"start",
            }
            return render(request,'html/dashboard/admin/addUser.html',context)
    # @login_required(login_url='/login')
    def add_user_submit(request):
            check = User.objects.filter(username=request.POST["username"]).first()
            if(check is None):
                newUser = User.objects.create_user(username=request.POST["username"],password=int(request.POST["idNumber"]), first_name=request.POST["firstName"],last_name = request.POST["lastName"],email=request.POST["email"],role=request.POST["role"],phone=int(request.POST["phone"]),mobile=int(request.POST["mobile"]),idCode=int(request.POST["idNumber"]),address=request.POST["address"])
                newUser.save()
                status = "User was created successfully!"
                if request.POST["role"] == "Teacher":
                    t = teacher(user=newUser)
                    t.save()
                elif request.POST["role"]=="Student":
                    s = student(user=newUser)
                    s.save()
                ok = 1
            else:
                status = "Username already exists!"
                ok = 0
            data = {
                'ok':ok,
                'status':status,
            }
            return JsonResponse(data)
    # @login_required(login_url='/login')
    def validate_username(request):
            username = request.GET.get('username',None)
            exists = User.objects.filter(username=username).exists()
            if(exists):
                data={
                    'msg':"Username taken!",
                    'status':0,
                }
            else:
                data={
                    'msg':"Username valid!",
                    'status':200,
                }
            return JsonResponse(data)
    # @login_required(login_url='/login')

    # @login_required(login_url='/login')
    def add_term(request):
            return render(request,'html/dashboard/admin/addTerm.html')
    # @login_required(login_url='/login')
    def add_term_submit(request):
            check = term.objects.filter(year=request.POST["year"],season=request.POST["season"],part=request.POST["part"]).first()
            if(check is None):
                newTerm = term(year=request.POST["year"],season=request.POST["season"],part=request.POST["part"])
                newTerm.save()
                status = f"<b>Term was added successfully:</b><br/>Year: {newTerm.year}<br/>Season: {newTerm.season}<br/>Part: {newTerm.part}"
            else:
                status = f"<b>Term already exists:</b><br/>Year: {check.year}<br/>Season: {check.season}<br/>Part: {check.part}"
            data = {
                'status':status,
            }
            return JsonResponse(data)

    # @login_required(login_url='/login')
    def new_course(request):
            return render(request,'html/dashboard/admin/newCourse.html')
    # @login_required(login_url='/login')
    def new_course_submit(request):
            new = course_info(course_name=request.POST['courseName'],code=request.POST['courseCode'])
            exist = [course_info.objects.filter(course_name=request.POST['courseName']).first(),course_info.objects.filter(code=request.POST['courseCode']).first()]
            if exist[0] is not None and exist[1] is not None:
                msg = f"<b>Course already exists:</b><br/>Name: {exist[0].course_name}<br/>Code: {exist[0].course_name}"
                status = 0
            elif exist[0] is not None:
                msg = f"<b>Name taken:</b><br/>Name: {exist[0].course_name}<br/>Code: {exist[0].course_name}"
                status = 0
            elif exist[1] is not None:
                msg = f"<b>Code taken:</b><br/>Name: {exist[1].course_name}<br/>Code: {exist[1].course_name}"
                status = 0
            else:
                msg = "Course created successfully!"
                status = 200
                new.save()
            data={
                'msg':msg,
                'status':status,
            }
            return JsonResponse(data)

    # @login_required(login_url='/login')
    def course_to_term(request):
            terms = []
            for i in term.objects.all():
                terms.append(i.getTermInfo())
            if terms:
                sortTerms(terms)
            data = {
                'terms':terms,
            }
            return render(request,'html/dashboard/admin/courseToTerm.html',data)
    # @login_required(login_url='/login')
    def course_to_term_submit(request):
            newTerm = request.POST['term'].split("-")
            newTerm = term.objects.get(year=newTerm[2],season=newTerm[0],part=newTerm[1])
            newCourse = course_info.objects.get(code=request.POST['courseCode'])
            newTeacher = teacher.objects.get(user__username=request.POST['teacherUsername'])
            newGroup = request.POST['courseGroup']
            newCourse = course(term=newTerm,teacher=newTeacher,courseInfo=newCourse,group=newGroup)
            newCourse.save()
            data = {
                'msg':f"Course added to {request.POST['term']} successfully!",
                'status':200
            }
            return JsonResponse(data)
    # @login_required(login_url='/login')
    def auto_fill(request):
            answer = None
            thing = [request.GET.get('info',None),request.GET.get('wanted',None)]
            if thing[1] == "courseCode":
                answer = course_info.objects.filter(course_name=thing[0]).first()
                if answer is not None:
                    data = {
                    'info':answer.code,
                    'status':200,
                    }
            elif thing[1] == "courseName":
                answer = course_info.objects.filter(code=thing[0]).first()
                if answer is not None:
                    data = {
                    'info':answer.course_name,
                    'status':200,
                    }
            elif thing[1] == "teacherUsername":
                teachers = teacher.objects.all()
                for i in teachers:
                    temp = i.user.first_name + " " +i.user.last_name
                    if temp == thing[0]:
                        data = {
                        'info':i.user.username,
                        'status':200,
                        }
                        answer = 1
                        break
            elif thing[1] == "teacherName":
                answer = teacher.objects.filter(user__username=thing[0]).first()
                if answer is not None:
                    data = {
                    'info':answer.user.first_name + " " +answer.user.last_name,
                    'status':200,
                    }
            if answer is None:
                data = {
                'info':"Not found",
                'status':0,
                }
            return JsonResponse(data)

    # @login_required(login_url='/login')
    def students_to_course(request):
            terms = []
            for i in term.objects.all():
                terms.append(i.getTermInfo())
            if terms:
                sortTerms(terms)
            data = {
                'terms':terms,
            }
            return render(request,'html/dashboard/admin/studentToCourse.html',data)
    # @login_required(login_url='/login')
    def getTermCourse(request):
            myterm = request.GET.get('info',None).split("-")
            myterm = term.objects.get(year=myterm[2],season=myterm[0],part=myterm[1])
            courses = []
            for i in myterm.courses.all():
                courses.append(i.getCourseInfo())
            courses.sort(key=lambda i: i['course_name'])
            data = {
                'courses':courses
            }
            return JsonResponse(data)
    # @login_required(login_url='/login')
    def students_to_course_submit(request):
            myterm = [request.POST['term'].split('-')[0],int(request.POST['term'].split('-')[1]),int(request.POST['term'].split('-')[2])]
            mycourse = [request.POST['courses'].split(' - ')[0],request.POST['courses'].split(' - ')[1].split(':')[1],int(request.POST['courses'].split(' - ')[2].split(':')[1])]
            mycourse = course.objects.get(courseInfo__course_name = mycourse[0],courseInfo__code = mycourse[1],group = mycourse[2],term__year=myterm[2],term__season=myterm[0],term__part=myterm[1])
            names = list(filter(None,request.POST['studentNames'].split('\n')))
            students = student.objects.all()
            for i in names:
                toAdd = list(filter(lambda x: x.user.first_name+" "+x.user.last_name==i,students))
                toAdd[0].course.add(mycourse)
                toAdd[0].save()
            data = {
            'msg':f"<b>Students added to the course successfully!</b><br/>Course name: {mycourse.courseInfo.course_name}<br/>Course students number: {len(mycourse.students.all())}",
            'status':200
            }
            return JsonResponse(data)
    # @login_required(login_url='/login')
    def validate_usernames(request):
            names = list(filter(None,request.GET.get('info',None).split(",")))
            response = []
            for i in names:
                students = student.objects.all()
                toAdd = list(filter(lambda x: x.user.first_name+" "+x.user.last_name==i,students))
                if toAdd:
                        response.append({'name':toAdd[0].user.first_name +" "+toAdd[0].user.last_name,'status':200})
                else:
                    response.append({'name':i,'status':0})
            data = {
                'response':response,
                'status':200
            }
            return JsonResponse(data)

    # @login_required(login_url='/login')
    def get_users(request):
            return render(request,'html/dashboard/admin/get_users.html')
    # @login_required(login_url='/login')
    def get_users_ajax(request):
            type = request.POST["type"]
            active = request.POST["active"]
            if type == "All":
                if active == "Active":
                    users = serializers.serialize("json", User.objects.filter(is_active = True))
                elif active == "Deactive":
                    users = serializers.serialize("json", User.objects.filter(is_active = False))
                else:
                    users = serializers.serialize("json", User.objects.all())
            elif type == "Teachers":
                if active == "Active":
                    users = serializers.serialize("json", User.objects.filter(role="Teacher",is_active=True))
                elif active == "Deactive":
                    users = serializers.serialize("json", User.objects.filter(role="Teacher",is_active=False))
                else:
                    users = serializers.serialize("json", User.objects.filter(role="Teacher"))
            elif type == "Students":
                if active == "Active":
                    users = serializers.serialize("json", User.objects.filter(role="Student",is_active=True))
                elif active == "Deactive":
                    users = serializers.serialize("json", User.objects.filter(role="Student",is_active=False))
                else:
                    users = serializers.serialize("json", User.objects.filter(role="Student"))
            else:
                if active == "Active":
                    users = serializers.serialize("json", User.objects.filter(is_active=True).exclude(role="Teacher").exclude(role="Student"))
                elif active == "Deactive":
                    users = serializers.serialize("json", User.objects.filter(is_active=False).exclude(role="Teacher").exclude(role="Student"))
                else:
                    users = serializers.serialize("json", User.objects.all().exclude(role="Teacher").exclude(role="Student"))
            data = {
                'users':users
            }
            return JsonResponse(data)

    # @login_required(login_url='/login')
    def get_courses(request):
            return render(request,'html/dashboard/admin/get_courses.html')
    # @login_required(login_url='/login')
    def get_courses_ajax(request):
        if request.POST["year"]=='All':
            year = 1
        else:
            year = int(request.POST["year"])
        if request.POST["season"]=='All':
            season = ''
        else:
            season = request.POST["season"]
        if request.POST["part"]=='All':
            part = ''
        else:
            part = int(request.POST["part"])
        courses = course.objects.filter(term__year__contains = year,term__season__contains=season,term__part__contains=part)
        list = []
        for i in courses:
            list.append({'name':i.courseInfo.course_name,'code':i.courseInfo.code,'term':{'year':i.term.year,'season':i.term.season,'part':i.term.part},'group':i.group,'num':len(i.students.all())})
        data = {
            'courses':list
        }
        return JsonResponse(data)
    def get_info(request,info):
        requested = request
        requested.user = User.objects.get(username = info)
        requested.content_params['admin'] = True
        if requested.user.role == "Student":
            scores = studentViews.studentScore(requested)['tree']
            context = {
                'user':serializers.serialize("json",User.objects.filter(username = info)),
                'tree':scores
            }
        elif requested.user.role == "Teacher":
            courses = getCourse(requested)
            context = {
                'user':serializers.serialize("json",User.objects.filter(username = info)),
                'courses':courses
            }
        else:
            context = {
                'user':serializers.serialize("json",User.objects.filter(username = info)),
            }
        return JsonResponse(context)
