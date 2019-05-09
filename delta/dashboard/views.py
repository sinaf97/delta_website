import json , copy , manage , uuid ,shutil , os
from django.shortcuts import render
from .models import term , course,score,student,User,teacher,massege
from .models import courseInfo as course_info
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
from django.core import serializers
from .methods import *
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .decoratore import *
from bookShelf.models import book,date,bookGroup
from django.template import loader, RequestContext


class default:
    @login_required(login_url='/login')
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
                # return render (request,"html/dashboard/admin/dashboard_a.html",context)
                return render (request,"html/dashboard/admin/dashboard_a.html",context)

    @login_required(login_url='/login')
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
    @login_required(login_url='/login')
    def change_name(request):
            request.user.first_name = request.POST["firstName"]
            request.user.last_name = request.POST["lastName"]
            request.user.save()
            context = {
                'status':200,
                'new_name':request.user.get_full_name(),
                'msg':"Name changed successfully"
            }
            return JsonResponse(context)
    @login_required(login_url='/login')
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
        'status':200,
            'msg': msg
            }
        return JsonResponse(context)
    @login_required(login_url='/login')
    def change_profile_photo(request):
        try:
            pic = request.FILES["pic"]
            change_photo(request.user,pic)
            msg = 'Profile Photo changed successfully'
        except:
            request.user.pic = 'default/profile.png'
            request.user.save()
            msg = 'Profile Photo was deleted!'

        context = {
        'status':200,
            'msg':msg,
            'path':request.user.pic.url
        }
        return JsonResponse(context)
    @login_required(login_url='/login')
    def inbox(request):
        if request.user.role == "Teacher":
            return teacherViews.r_massege(request)
        elif request.user.role == "Student":
            return studentViews.r_massege(request)
        else:
            return adminViews.r_massege(request)

    def inbox_seen(request):
        m = massege.objects.get(id = request.GET.get('id'))
        m.seen = True
        m.save()
        data = {
            'status':200
        }
        return JsonResponse(data)

    def compose(request,username = None):
        if request.user.role == "Teacher":
            return teacherViews.s_massege(request,username)
        elif request.user.role == "Student":
            return studentViews.s_massege(request,username)
        else:
            return adminViews.s_massege(request,username)

    def mail_send(request):
        try:
            receiver = User.objects.get(username=request.POST['username'])
        except Exception as e:
            data = {
                'status':0,
                'msg':"User not found"
            }
            return JsonResponse(data)
        if request.user.role == "Student" and receiver.role == "Student":
            data = {
                'status':210,
                'msg':"Insufficaint autharity"
            }
        else:
            m = massege(id = uuid.uuid1().hex ,origin=request.user,to=receiver,subject = request.POST['subject'],text=request.POST['text'],seen=False)
            m.save()
            data = {
            'status':200,
            'msg':"massege sent successfully"
            }
        return JsonResponse(data)

    def mail_delete(request):
        m = massege.objects.get(id = request.GET.get('id'))
        m.delete()
        data = {
            'status':200,
            'msg':'Mail was removed successfully'
        }
        return JsonResponse(data)

class studentViews:
    @login_required(login_url='/login')
    @role_required(allowed_roles=['Student'])
    def studentScore(request,user = None):
        if(user is not None):
            scores = user['user'].student.scores.all()
        else:
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
        return render(request,"html/dashboard/student/score.html",context)
    @login_required(login_url='/login')
    @role_required(allowed_roles=['Student'])
    def s_massege(request,username = None):
        if username is None:
            username = ""
        return render(request,'html/dashboard/student/compose.html',{'username':username})
    @login_required(login_url='/login')
    @role_required(allowed_roles=['Student'])
    def r_massege(request):
        return render(request,'html/dashboard/student/inbox.html',get_masseges(request))
    @login_required(login_url='/login')
    @role_required(allowed_roles=['Student'])
    def reports(request):
            return render(request,'html/dashboard/student/reports.html')
    @login_required(login_url='/login')
    @role_required(allowed_roles=['Student'])
    def info(request):
        data = {
            'user':request.user
        }
        return render (request,"html/dashboard/student/info.html",data)

class teacherViews:
    @login_required(login_url='/login')
    @role_required(allowed_roles=['Teacher'])
    def courses(request):
            context = getCourse(request)
            return render(request,'html/dashboard/teacher/courses.html',context)
    @login_required(login_url='/login')
    @role_required(allowed_roles=['Teacher'])
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
            if 'admin' not in request.content_params.keys():
                return render(request,'html/dashboard/teacher/courseInfo.html',context)
            return context
    @login_required(login_url='/login')
    @role_required(allowed_roles=['Teacher'])
    def add_score(request):
            info = request.POST["course"]
            theCourse = courseConverter(info)
            students = theCourse.students.all()
            for i in students:
                midScore = request.POST[("midterm_"+i.user.username)]
                finalScore = request.POST[("final_"+i.user.username)]
                teacherViews.commiteScore(request,theCourse,i.user.username,midScore,finalScore)
            data = {
                'msg':"Scores submitted successfully"
            }
            return JsonResponse(data)
    @login_required(login_url='/login')
    @role_required(allowed_roles=['Teacher'])
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
    @login_required(login_url='/login')
    @role_required(allowed_roles=['Teacher'])
    def info(request):
            data = {
                'user':request.user,
                'courses':getCourse(request)
            }
            return render (request,"html/dashboard/teacher/info.html",data)
    @login_required(login_url='/login')
    @role_required(allowed_roles=['Teacher'])
    def r_massege(request):
        return render(request,'html/dashboard/teacher/inbox.html',get_masseges(request))
    def s_massege(request,username = None):
        if username is None:
            username = ""
        return render(request,'html/dashboard/teacher/compose.html',{'username':username})

class adminViews:
    def r_massege(request):
        return render(request,'html/dashboard/admin/inbox.html',get_masseges(request))
    def s_massege(request,username = None):
        if username is None:
            username = ""
        return render(request,'html/dashboard/admin/compose.html',{'username':username})
    @login_required(login_url='/login')
    @role_blocked(blocked_roles=['Teacher','Student'])
    def add_user(request):
            context = {
                'status':"start",
            }
            return render(request,'html/dashboard/admin/addUser.html',context)
    @login_required(login_url='/login')
    @role_blocked(blocked_roles=['Teacher','Student'])
    def add_user_submit(request):
            check = User.objects.filter(username=request.POST["username"]).first()
            if(check is None):
                newUser = User.objects.create_user(username=request.POST["username"],password=int(request.POST["idNumber"]),first_name=request.POST["firstName"],last_name = request.POST["lastName"],email=request.POST["email"],role=request.POST["role"],phone=int(request.POST["phone"]),mobile=int(request.POST["mobile"]),idCode=int(request.POST["idNumber"]),address=request.POST["address"])
                try:
                    pic = request.FILES["pic"]
                    fs = FileSystemStorage()
                    fs.save(picPath(newUser,pic.name),pic)
                    newUser.pic = picPath(newUser,pic.name)
                except:
                    pass
                newUser.save()
                msg = "User was created successfully!"
                if request.POST["role"] == "Teacher":
                    t = teacher(user=newUser)
                    t.save()
                elif request.POST["role"]=="Student":
                    s = student(user=newUser)
                    s.save()
                status = 1
            else:
                msg = "Username already exists!"
                status = 0
            data = {
                'status':status,
                'msg':msg,
            }
            return JsonResponse(data)
    @login_required(login_url='/login')
    @role_blocked(blocked_roles=['Teacher','Student'])
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

    @login_required(login_url='/login')
    @role_blocked(blocked_roles=['Teacher','Student'])
    def add_term(request):
            return render(request,'html/dashboard/admin/addTerm.html')
    @login_required(login_url='/login')
    @role_blocked(blocked_roles=['Teacher','Student'])
    def add_term_submit(request):
            check = term.objects.filter(year=request.POST["year"],season=request.POST["season"],part=request.POST["part"]).first()
            if(check is None):
                newTerm = term(year=request.POST["year"],season=request.POST["season"],part=request.POST["part"])
                newTerm.save()
                msg = f"<b>Term was added successfully:</b><br/>Year: {newTerm.year}<br/>Season: {newTerm.season}<br/>Part: {newTerm.part}"
                status = 1
            else:
                msg = f"<b>Term already exists:</b><br/>Year: {check.year}<br/>Season: {check.season}<br/>Part: {check.part}"
                status = 0
            data = {
                'msg' : msg,
                'status':status,
            }
            return JsonResponse(data)

    @login_required(login_url='/login')
    @role_blocked(blocked_roles=['Teacher','Student'])
    def new_course(request):
            return render(request,'html/dashboard/admin/newCourse.html')
    @login_required(login_url='/login')
    @role_blocked(blocked_roles=['Teacher','Student'])
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

    @login_required(login_url='/login')
    @role_blocked(blocked_roles=['Teacher','Student'])
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
    @login_required(login_url='/login')
    @role_blocked(blocked_roles=['Teacher','Student'])
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
    @login_required(login_url='/login')
    @role_blocked(blocked_roles=['Teacher','Student'])
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

    @login_required(login_url='/login')
    @role_blocked(blocked_roles=['Teacher','Student'])
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
    @login_required(login_url='/login')
    @role_blocked(blocked_roles=['Teacher','Student'])
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
    @login_required(login_url='/login')
    @role_blocked(blocked_roles=['Teacher','Student'])
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
    @login_required(login_url='/login')
    @role_blocked(blocked_roles=['Teacher','Student'])
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

    @login_required(login_url='/login')
    @role_blocked(blocked_roles=['Teacher','Student'])
    def get_users(request):
            return render(request,'html/dashboard/admin/get_users.html')
    @login_required(login_url='/login')
    @role_blocked(blocked_roles=['Teacher','Student'])
    def get_users_ajax(request):
            type = request.POST["type"]
            active = request.POST["active"]
            name = [request.POST["name"],request.POST["last_name"]]
            if type == "All":
                if active == "Active":
                    users = serializers.serialize("json", User.objects.filter(is_active = True,first_name__contains = name[0],last_name__contains=name[1]))
                elif active == "Deactive":
                    users = serializers.serialize("json", User.objects.filter(is_active = False,first_name__contains = name[0],last_name__contains=name[1]))
                else:
                    users = serializers.serialize("json", User.objects.filter(first_name__contains = name[0],last_name__contains=name[1]))
            elif type == "Teachers":
                if active == "Active":
                    users = serializers.serialize("json", User.objects.filter(role="Teacher",is_active=True,first_name__contains = name[0],last_name__contains=name[1]))
                elif active == "Deactive":
                    users = serializers.serialize("json", User.objects.filter(role="Teacher",is_active=False,first_name__contains = name[0],last_name__contains=name[1]))
                else:
                    users = serializers.serialize("json", User.objects.filter(role="Teacher",first_name__contains = name[0],last_name__contains=name[1]))
            elif type == "Students":
                if active == "Active":
                    users = serializers.serialize("json", User.objects.filter(role="Student",is_active=True,first_name__contains = name[0],last_name__contains=name[1]))
                elif active == "Deactive":
                    users = serializers.serialize("json", User.objects.filter(role="Student",is_active=False,first_name__contains = name[0],last_name__contains=name[1]))
                else:
                    users = serializers.serialize("json", User.objects.filter(role="Student",first_name__contains = name[0],last_name__contains=name[1]))
            else:
                if active == "Active":
                    users = serializers.serialize("json", User.objects.filter(is_active=True,first_name__contains = name[0],last_name__contains=name[1]).exclude(role="Teacher").exclude(role="Student"))
                elif active == "Deactive":
                    users = serializers.serialize("json", User.objects.filter(is_active=False,first_name__contains = name[0],last_name__contains=name[1]).exclude(role="Teacher").exclude(role="Student"))
                else:
                    users = serializers.serialize("json", User.objects.filter(first_name__contains = name[0],last_name__contains=name[1]).exclude(role="Teacher").exclude(role="Student"))
            data = {
                'users':users
            }
            return JsonResponse(data)

    @login_required(login_url='/login')
    @role_blocked(blocked_roles=['Teacher','Student'])
    def get_courses(request):
            return render(request,'html/dashboard/admin/get_courses.html')
    @login_required(login_url='/login')
    @role_blocked(blocked_roles=['Teacher','Student'])
    def get_courses_ajax(request):
        courses = course.objects.filter(courseInfo__course_name__contains = request.POST["name"] ,term__year__contains = request.POST["year"],term__season__contains=request.POST["season"],term__part__contains=request.POST["part"])
        list = []
        for i in courses:
            list.append({'name':i.courseInfo.course_name,'code':i.courseInfo.code,'term':{'year':i.term.year,'season':i.term.season,'part':i.term.part},'group':i.group,'num':len(i.students.all())})
        data = {
            'courses':list
        }
        return JsonResponse(data)
    @login_required(login_url='/login')
    @role_blocked(blocked_roles=['Teacher','Student'])
    def get_info(request,info):
        requested = request
        requested.user = User.objects.get(username = info)
        requested.content_params['admin'] = True
        if requested.user.role == "Student":
            context = {
                'user':serializers.serialize("json",User.objects.filter(username = info)),
                'scores':studentViews.studentScore(requested)
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
            print(context)
        return JsonResponse(context)

    @login_required(login_url='/login')
    @role_blocked(blocked_roles=['Teacher','Student'])
    def get_course_info(request,info):
        course = courseConverter(info)
        students = course.students.all()
        list = []
        for i in students:
            try:
                list.append({'user':serializers.serialize("json",[i.user]),'score':serializers.serialize("json",[i.scores.get(course=course)])})
            except:
                list.append({'user': serializers.serialize("json", [i.user]),'score': json.dumps([{'fields':{'midScore':0,'finalScore':0}}])})
        data = {
        'course':serializers.serialize("json",[course.courseInfo]),
        'students':list,
        'teacher':serializers.serialize("json",[course.teacher.user]),
        'term':course.term.getTermInfo(),
        'group':course.group,
        }
        return JsonResponse(data)

    @login_required(login_url='/login')
    @role_blocked(blocked_roles=['Teacher','Student'])
    def edit_user(request,info):
        user = User.objects.get(username = info)
        if user.role == "Student":
            context = {
                'euser':User.objects.get(username = info),
                'scores':studentViews.studentScore(request,{'user':user})
            }
        elif user.role == "Teacher":
            courses = getCourse(user)
            context = {
                'euser':User.objects.get(username = info),
                'courses':courses
            }
        else:
            context = {
                'euser':User.objects.get(username = info),
            }
        return render(request,'html/dashboard/admin/edit_user.html',context)
    @login_required(login_url='/login')
    @role_blocked(blocked_roles=['Teacher','Student'])
    def edit_user_ajax(request,info):
        user = User.objects.get(username=info)

        User.objects.filter(username=info).update(first_name=request.POST["fn"],\
        last_name=request.POST["ln"],\
        email=request.POST["em"],\
        phone=request.POST["ph"],\
        mobile=request.POST["mb"],\
        idCode=request.POST["id"],\
        address=request.POST["ad"])
        try:
            pic = request.FILES["pic"]
            change_photo(user,pic)
        except Exception as e:
            print(e)
        data = {
            'status':200,
            'msg':"User information successfully changed",
            'new_path':user.pic.url
        }
        return JsonResponse(data)
    @login_required(login_url='/login')
    @role_blocked(blocked_roles=['Teacher','Student'])
    def book_shelf(request):
        book_groups = bookGroup.objects.all()
        context = {
            'groups':book_groups
        }
        return render(request,'html/dashboard/admin/bookShelf/index.html',context);
