from .models import term , course,score,student,User,teacher
from django.core.files.storage import FileSystemStorage
import shutil , os
import manage



def courseConverter(info):
    info = info.split("_")
    info[1] = int(info[1])
    info[2] = int(info[2])
    info[4] = int(info[4])
    theCourse = course.objects.filter(courseInfo__code=info[0],group=info[1])
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
    try:
        t_courses = request.user.teacher.courses.all()
    except Exception as e:
        t_courses = request.teacher.courses.all()
    list = []
    for i in t_courses:
        list.append(i.getCourseInfo())
        sortCourses(list)
    return list

def sortCourses(list):
    list.sort(key=lambda i: i['term']['part'],reverse=True)
    list.sort(key=lambda i: i['term']['season'],reverse=True)
    list.sort(key=lambda i: i['term']['year'],reverse=True)
def sortCourses_name(list):
    list.sort(key=lambda i: i['part'],reverse=True)
    list.sort(key=lambda i: i['season'],reverse=True)
    list.sort(key=lambda i: i['year'],reverse=True)
def sortTerms(list):
    list.sort(key=lambda i: i['part'],reverse=True)
    list.sort(key=lambda i: i['season'],reverse=True)
    list.sort(key=lambda i: i['year'],reverse=True)

def studentScore(request,user):
        scores = user.student.scores.all()
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
        return context

def change_photo(user,pic):
    fs = FileSystemStorage()
    try:
        shutil.rmtree(os.path.dirname(manage.__file__)+'/media/users/'+user.role+'s/'+user.username+'/profile pic')
    except Exception as e:
        print(e)
    fs.save(picPath(user,pic.name),pic)
    user.pic = picPath(user,pic.name)
    user.save()

def picPath(user,fileName):
    fileName = fileName.split('.')[1]
    return f"users/{user.role}s/{user.username}/profile pic/{user.username}.{fileName}"
