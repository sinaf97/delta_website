import json , copy , manage , uuid ,shutil , os
from django.shortcuts import render
from .models import *
from .decoratore import *
from .methods import *
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from bookShelf.models import Book,Date,BookGroup
from django.template import loader, RequestContext
import base64
from PIL import Image

media_path = '/Users/sinafarahani/Desktop/Me/django/delta_fa'

class default:
    @login_required(login_url='/login')
    def dashboard(request,lang="fa"):
        context = {
            "user" : request.user,
        }
        if request.user.latin_role=="Student":
            context['info'] = {
            'term':Term.objects.last(),
            'course':request.user.student.course.filter(term = Term.objects.last()).first(),
            'score': request.user.student.scores.filter(course = request.user.student.course.filter(term = Term.objects.last()).first()).first()
            }
            return render(request,lang+"/html/dashboard/student/dashboard_s.html",context)
        elif request.user.latin_role=="Teacher":
            lastTerm = []
            for i in Term.objects.all():
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
            'courses' : getCourse(request,lang),
            'lastTerm':lastTerm
            }
            return render (request,lang+"/html/dashboard/teacher/dashboard_t.html",context)
        else:
            # return render (request,lang+"/html/dashboard/admin/dashboard_a.html",context)
            return render (request,lang+"/html/dashboard/admin/dashboard_a.html",context)

    @login_required(login_url='/login')
    def settings(request,lang="fa"):
        if request.user.latin_role == "Teacher":
            context = {
            'courses' : getCourse(request,lang="fa"),
            }
            return render(request,lang+"/html/dashboard/teacher/settings.html",context)
        elif request.user.latin_role == "Student":
            return render(request,lang+"/html/dashboard/student/settings.html")
        else:
            return render(request,lang+"/html/dashboard/admin/settings.html")
    @login_required(login_url='/login')
    def change_name(request,lang="fa"):
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
    def change_pass(request,lang="fa"):
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
    def change_profile_photo(request,lang="fa",newUser = None):
        if newUser is not None:
            user = newUser
        else:
            user = request.user
        try:
            picPath = request.POST["pic-path"]
            pic = Image.open(picPath[1:])
            change_photo(user,pic)
            os.remove(media_path+picPath)
            status = 200
            msg = 'Profile Photo changed successfully'
        except Exception as e:
            print(e)
            user.pic = 'default/profile.png'
            user.save()
            msg = 'Profile Photo was deleted!'
            status = 0
        finally:
            context = {
                'status':status,
                'msg':msg,
                'path':user.pic.url
            }
        return JsonResponse(context)
    @login_required(login_url='/login')
    def inbox(request,lang="fa"):
        if request.user.latin_role == "Teacher":
            return teacherViews.r_massege(request,lang)
        elif request.user.latin_role == "Student":
            return studentViews.r_massege(request,lang)
        else:
            return adminViews.r_massege(request,lang)

    def inbox_seen(request,lang="fa"):
        m = Massege.objects.get(id = request.GET.get('id'))
        m.seen = True
        m.save()
        data = {
            'status':200
        }
        return JsonResponse(data)

    def compose(request,lang="fa",username = None):
        if request.user.latin_role == "Teacher":
            return teacherViews.s_massege(request,lang,username)
        elif request.user.latin_role == "Student":
            return studentViews.s_massege(request,lang,username)
        else:
            return adminViews.s_massege(request,lang,username)

    def mail_send(request,lang="fa"):
        try:
            receiver = User.objects.get(username=request.POST['username'])
        except Exception as e:
            data = {
                'status':0,
                'msg':"User not found"
            }
            return JsonResponse(data)
        if request.user.latin_role == "Student" and receiver.latin_role == "Student":
            data = {
                'status':210,
                'msg':"Insufficaint autharity"
            }
        else:
            m = Massege(id = uuid.uuid1().hex ,origin=request.user,to=receiver,subject = request.POST['subject'],text=request.POST['text'],seen=False)
            m.save()
            data = {
            'status':200,
            'msg':"massege sent successfully"
            }
        return JsonResponse(data)

    def mail_delete(request,lang="fa"):
        m = Massege.objects.get(id = request.GET.get('id'))
        m.delete()
        data = {
            'status':200,
            'msg':'Mail was removed successfully'
        }
        return JsonResponse(data)

    @login_required(login_url='/login')
    def save_image_ajax(request,lang="fa"):
            img = request.POST['img']
            url = save_photo(img)
            data = {
                'url': url
            }
            return JsonResponse(data)

class studentViews:
    @login_required(login_url='/login')
    @role_required(allowed_roles=['Student'])
    def studentScore(request,lang = "fa",user = None):
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
        return render(request,lang+"/html/dashboard/student/score.html",context)
    @login_required(login_url='/login')
    @role_required(allowed_roles=['Student'])
    def s_massege(request,lang,username = None):
        if username is None:
            username = ""
        return render(request,lang+'/html/dashboard/student/compose.html',{'username':username})
    @login_required(login_url='/login')
    @role_required(allowed_roles=['Student'])
    def r_massege(request,lang="fa"):
        return render(request,lang+'/html/dashboard/student/inbox.html',get_masseges(request,lang))
    @login_required(login_url='/login')
    @role_required(allowed_roles=['Student'])
    def reports(request,lang="fa"):
            return render(request,lang+'/html/dashboard/student/reports.html')
    @login_required(login_url='/login')
    @role_required(allowed_roles=['Student'])
    def info(request,lang="fa"):
        data = {
            'user':request.user
        }
        return render (request,lang+"/html/dashboard/student/info.html",data)

class teacherViews:
    @login_required(login_url='/login')
    @role_required(allowed_roles=['Teacher'])
    def courses(request,lang="fa"):
            context = getCourse(request,lang)
            return render(request,lang+'/html/dashboard/teacher/courses.html',context)
    @login_required(login_url='/login')
    @role_required(allowed_roles=['Teacher'])
    def courseInfo(request,lang,info):
            theCourse = courseConverter(info)
            lastTerm = []
            for i in Term.objects.all():
                lastTerm.append(i.getTermInfo())
            sortTerms(lastTerm)
            lastTerm = lastTerm[-1]

            students = []
            for i in theCourse.students.all():
                if lang == 'en':
                    students.append(i.getStudentLatinInfo())
                else:
                    students.append(i.getStudentInfo())
            scores = []
            for i in theCourse.scores.all():
                scores.append(i.getScoreInfo())
            context = {
            'lastTerm':lastTerm,
            'rawInfo': theCourse,
            'info':theCourse.getCourseInfo(),
            'courses': getCourse(request,lang),
            'students':students,
            'scores':scores,
            }
            if 'admin' not in request.content_params.keys():
                return render(request,lang+'/html/dashboard/teacher/courseInfo.html',context)
            return context
    @login_required(login_url='/login')
    @role_required(allowed_roles=['Teacher'])
    def add_score(request,lang="fa"):
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
            std = Student.objects.filter(user__username=username).first()
            new = Score(student=std,course=theCourse,midScore=midscore,finalScore=finalscore)
            exist = Score.objects.filter(student=std,course=theCourse).first()
            if exist is None:
                new.save()
            else:
                Score.objects.filter(student=std,course=theCourse).update(midScore=midscore,finalScore=finalscore)
    @login_required(login_url='/login')
    @role_required(allowed_roles=['Teacher'])
    def info(request,lang="fa"):
            data = {
                'user':request.user,
                'courses':getCourse(request,lang)
            }
            return render (request,lang+"/html/dashboard/teacher/info.html",data)
    @login_required(login_url='/login')
    @role_required(allowed_roles=['Teacher'])
    def r_massege(request,lang="fa"):
        return render(request,lang+'/html/dashboard/teacher/inbox.html',get_masseges(request,lang))
    def s_massege(request,lang,username = None):
        if username is None:
            username = ""
        return render(request,lang+'/html/dashboard/teacher/compose.html',{'username':username})

class adminViews:
    def r_massege(request,lang="fa"):
        return render(request,lang+'/html/dashboard/admin/inbox.html',get_masseges(request,lang))
    def s_massege(request,lang,username = None):
        if username is None:
            username = ""
        return render(request,lang+'/html/dashboard/admin/compose.html',{'username':username})
    @login_required(login_url='/login')
    @role_blocked(blocked_roles=['Teacher','Student'])
    def add_user(request,lang="fa"):
            context = {
                'status':"start",
            }
            return render(request,lang+'/html/dashboard/admin/addUser.html',context)
    @login_required(login_url='/login')
    @role_blocked(blocked_roles=['Teacher','Student'])
    def add_user_submit(request,lang="fa"):
            check = User.objects.filter(username=request.POST["username"]).first()
            if(check is None):
                newUser = User.objects.create_user(username=request.POST["username"],password=int(request.POST["idNumber"]),first_name=request.POST["firstName"],last_name = request.POST["lastName"],email=request.POST["email"],latin_role=request.POST["role"],phone=int(request.POST["phone"]),mobile=int(request.POST["mobile"]),idCode=int(request.POST["idNumber"]),address=request.POST["address"])
                try:
                    default.change_profile_photo(request,lang,newUser)
                except Exception as e:
                    print(e)
                    pass
                newUser.save()
                msg = "User was created successfully!"
                if request.POST["role"] == "Teacher":
                    t = Teacher(user=newUser)
                    t.save()
                elif request.POST["role"]=="Student":
                    s = Student(user=newUser)
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
    def validate_username(request,lang="fa"):
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
    def add_term(request,lang="fa"):
            return render(request,lang+'/html/dashboard/admin/addTerm.html')
    @login_required(login_url='/login')
    @role_blocked(blocked_roles=['Teacher','Student'])
    def add_term_submit(request,lang="fa"):
            check = Term.objects.filter(year=request.POST["year"],season=request.POST["season"],part=request.POST["part"]).first()
            if(check is None):
                newTerm = Term(year=request.POST["year"],season=request.POST["season"],part=request.POST["part"])
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
    def new_course(request,lang="fa"):
            return render(request,lang+'/html/dashboard/admin/newCourse.html')
    @login_required(login_url='/login')
    @role_blocked(blocked_roles=['Teacher','Student'])
    def new_course_submit(request,lang="fa"):
            new = CourseInfo(course_name=request.POST['courseName'],code=request.POST['courseCode'])
            exist = [CourseInfo.objects.filter(course_name=request.POST['courseName']).first(),CourseInfo.objects.filter(code=request.POST['courseCode']).first()]
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
    def course_to_term(request,lang="fa"):
            terms = []
            for i in Term.objects.all():
                terms.append(i.getTermInfo())
            if terms:
                sortTerms(terms)
            data = {
                'terms':terms,
            }
            return render(request,lang+'/html/dashboard/admin/courseToTerm.html',data)
    @login_required(login_url='/login')
    @role_blocked(blocked_roles=['Teacher','Student'])
    def course_to_term_submit(request,lang="fa"):
            newTerm = request.POST['term'].split("-")
            newTerm = Term.objects.get(year=newTerm[2],season=newTerm[0],part=newTerm[1])
            newCourse = CourseInfo.objects.get(code=request.POST['courseCode'])
            newTeacher = Teacher.objects.get(user__username=request.POST['teacherUsername'])
            newGroup = request.POST['courseGroup']
            newCourse = Course(term=newTerm,teacher=newTeacher,courseInfo=newCourse,group=newGroup)
            newCourse.save()
            data = {
                'msg':f"Course added to {request.POST['term']} successfully!",
                'status':200
            }
            return JsonResponse(data)
    @login_required(login_url='/login')
    @role_blocked(blocked_roles=['Teacher','Student'])
    def auto_fill(request,lang="fa"):
            answer = None
            thing = [request.GET.get('info',None),request.GET.get('wanted',None)]
            if thing[1] == "courseCode":
                answer = CourseInfo.objects.filter(course_name=thing[0]).first()
                if answer is not None:
                    data = {
                    'info':answer.code,
                    'status':200,
                    }
            elif thing[1] == "courseName":
                answer = CourseInfo.objects.filter(code=thing[0]).first()
                if answer is not None:
                    data = {
                    'info':answer.course_name,
                    'status':200,
                    }
            elif thing[1] == "teacherUsername":
                teachers = Teacher.objects.all()
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
                answer = Teacher.objects.filter(user__username=thing[0]).first()
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
    def students_to_course(request,lang="fa"):
            terms = []
            for i in Term.objects.all():
                terms.append(i.getTermInfo())
            if terms:
                sortTerms(terms)
            data = {
                'terms':terms,
            }
            return render(request,lang+'/html/dashboard/admin/studentToCourse.html',data)
    @login_required(login_url='/login')
    @role_blocked(blocked_roles=['Teacher','Student'])
    def getTermCourse(request,lang="fa"):
            myterm = request.GET.get('info',None).split("-")
            myterm = Term.objects.get(year=myterm[2],season=myterm[0],part=myterm[1])
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
    def students_to_course_submit(request,lang="fa"):
            myterm = [request.POST['term'].split('-')[0],int(request.POST['term'].split('-')[1]),int(request.POST['term'].split('-')[2])]
            mycourse = [request.POST['courses'].split(' - ')[0],request.POST['courses'].split(' - ')[1].split(':')[1],int(request.POST['courses'].split(' - ')[2].split(':')[1])]
            mycourse = Course.objects.get(courseInfo__course_name = mycourse[0],courseInfo__code = mycourse[1],group = mycourse[2],term__year=myterm[2],term__season=myterm[0],term__part=myterm[1])
            names = list(filter(None,request.POST['studentNames'].split('\n')))
            students = Student.objects.all()
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
    def validate_usernames(request,lang="fa"):
            names = list(filter(None,request.GET.get('info',None).split(",")))
            response = []
            for i in names:
                students = Student.objects.all()
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
    def get_users(request,lang="fa"):
            return render(request,lang+'/html/dashboard/admin/get_users.html')
    @login_required(login_url='/login')
    @role_blocked(blocked_roles=['Teacher','Student'])
    def get_users_ajax(request,lang="fa"):
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
                    users = serializers.serialize("json", User.objects.filter(latin_role="Teacher",is_active=True,first_name__contains = name[0],last_name__contains=name[1]))
                elif active == "Deactive":
                    users = serializers.serialize("json", User.objects.filter(latin_role="Teacher",is_active=False,first_name__contains = name[0],last_name__contains=name[1]))
                else:
                    users = serializers.serialize("json", User.objects.filter(latin_role="Teacher",first_name__contains = name[0],last_name__contains=name[1]))
            elif type == "Students":
                if active == "Active":
                    users = serializers.serialize("json", User.objects.filter(latin_role="Student",is_active=True,first_name__contains = name[0],last_name__contains=name[1]))
                elif active == "Deactive":
                    users = serializers.serialize("json", User.objects.filter(latin_role="Student",is_active=False,first_name__contains = name[0],last_name__contains=name[1]))
                else:
                    users = serializers.serialize("json", User.objects.filter(latin_role="Student",first_name__contains = name[0],last_name__contains=name[1]))
            else:
                if active == "Active":
                    users = serializers.serialize("json", User.objects.filter(is_active=True,first_name__contains = name[0],last_name__contains=name[1]).exclude(latin_role="Teacher").exclude(latin_role="Student"))
                elif active == "Deactive":
                    users = serializers.serialize("json", User.objects.filter(is_active=False,first_name__contains = name[0],last_name__contains=name[1]).exclude(latin_role="Teacher").exclude(latin_role="Student"))
                else:
                    users = serializers.serialize("json", User.objects.filter(first_name__contains = name[0],last_name__contains=name[1]).exclude(latin_role="Teacher").exclude(latin_role="Student"))
            data = {
                'users':users
            }
            return JsonResponse(data)

    @login_required(login_url='/login')
    @role_blocked(blocked_roles=['Teacher','Student'])
    def get_courses(request,lang="fa"):
            return render(request,lang+'/html/dashboard/admin/get_courses.html')
    @login_required(login_url='/login')
    @role_blocked(blocked_roles=['Teacher','Student'])
    def get_courses_ajax(request,lang="fa"):
        courses = Course.objects.filter(courseInfo__course_name__contains = request.POST["name"] ,term__year__contains = request.POST["year"],term__season__contains=request.POST["season"],term__part__contains=request.POST["part"])
        list = []
        for i in courses:
            list.append({'name':i.courseInfo.course_name,'code':i.courseInfo.code,'term':{'year':i.term.year,'season':i.term.season,'part':i.term.part},'group':i.group,'num':len(i.students.all())})
        data = {
            'courses':list
        }
        return JsonResponse(data)
    @login_required(login_url='/login')
    @role_blocked(blocked_roles=['Teacher','Student'])
    def get_info(request,lang,info):
        requested = request
        requested.user = User.objects.get(username = info)
        requested.content_params['admin'] = True
        if requested.user.role == "Student":
            context = {
                'user':serializers.serialize("json",User.objects.filter(username = info)),
                'scores':studentViews.studentScore(requested)
            }
        elif requested.user.role == "Teacher":
            courses = getCourse(requested,lang)
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
    def get_course_info(request,lang,info):
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
    def edit_user(request,lang,info):
        user = User.objects.get(username = info)
        if user.latin_role == "Student":
            context = {
                'euser':User.objects.get(username = info),
                'scores':studentViews.studentScore(request,{'user':user})
            }
        elif user.latin_role == "Teacher":
            courses = getCourse(user)
            context = {
                'euser':User.objects.get(username = info),
                'courses':courses
            }
        else:
            context = {
                'euser':User.objects.get(username = info),
            }
        return render(request,lang+'/html/dashboard/admin/edit_user.html',context)
    @login_required(login_url='/login')
    @role_blocked(blocked_roles=['Teacher','Student'])
    def edit_user_ajax(request,lang,info):
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
    def book_shelf(request,lang="fa"):
        book_groups = BookGroup.objects.all()
        context = {
            'groups':book_groups
        }
        return render(request,lang+'/html/dashboard/admin/bookShelf/index.html',context);
