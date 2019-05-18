from .models import *
from django.core.files.storage import FileSystemStorage
import shutil , os
import manage , uuid
from django.core.files.storage import default_storage
import base64
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import codecs
from pathlib import Path,PurePath

def courseConverter(info):
    info = info.split("_")
    info[1] = int(info[1])
    info[2] = int(info[2])
    info[4] = int(info[4])
    theCourse = Course.objects.filter(courseInfo__code=info[0],group=info[1])
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

def getCourse(request,lang):
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
    try:
        pic.save(Path(picPath(user,pic)))
        user.pic = picPath(user,pic)[6:]
        user.save()
    except Exception as e:
        print('change photo '+e)
        pass


def picPath(user,pic):
    try:
        os.makedirs(f"media/users/{user.latin_role}s/{user.username}/profile pic")
    except Exception as e:
        print(e)
        pass
    return f"media/users/{user.latin_role}s/{user.username}/profile pic/{user.username}.{pic.format.lower()}"

def save_photo(pic):
    pic = pic.split(',')
    imageType = pic[0].split(';')[0].split('/')[1]
    fs = FileSystemStorage()
    picPath = savePicPath(imageType)
    pic = codecs.encode(pic[1]+'=')
    with open('/Users/sinafarahani/Desktop/Me/django/delta_fa'+picPath, "wb") as fh:
        fh.write(base64.decodebytes(pic))
    return picPath

def savePicPath(imageType):
    # return f"/media/temp/profile images/{uuid.uuid1()}.jpg"
    return f"/media/temp/profile images/{uuid.uuid1()}.{imageType}"

def get_masseges(request,lang):
    m = Massege.objects.filter(to = request.user)
    mlist = []
    jlist = []
    counter = 0
    for ma in m:
        if ma.seen:
            seen = 1
        else:
            seen = 0
        if lang == "fa":
            mlist.append({'count':counter,'id':ma.id,'origin':{'name':ma.origin.get_full_name(),'username':ma.origin.username},'seen':ma.seen,'title':ma.subject,'text':ma.text,'time_sent':{'h':ma.time_sent.hour,'m':ma.time_sent.minute},'date_sent':ma.date_sent})
            jlist.append({'count':counter,'id':ma.id,'origin':{'name':ma.origin.get_full_name(),'username':ma.origin.username},'seen':seen,'title':ma.subject,'text':ma.text,'time_sent':{'h':ma.time_sent.hour,'m':ma.time_sent.minute},'date_sent':{'year':ma.date_sent.year,'month':ma.date_sent.month,'day':ma.date_sent.day}})
        else:
            mlist.append({'count':counter,'id':ma.id,'origin':{'name':ma.origin.latin_str(),'username':ma.origin.username},'seen':ma.seen,'title':ma.subject,'text':ma.text,'time_sent':{'h':ma.time_sent.hour,'m':ma.time_sent.minute},'date_sent':ma.date_sent})
            jlist.append({'count':counter,'id':ma.id,'origin':{'name':ma.origin.latin_str(),'username':ma.origin.username},'seen':seen,'title':ma.subject,'text':ma.text,'time_sent':{'h':ma.time_sent.hour,'m':ma.time_sent.minute},'date_sent':{'year':ma.date_sent.year,'month':ma.date_sent.month,'day':ma.date_sent.day}})
        counter+=1
    mlist.reverse()
    data = {
        'masseges' : mlist,
        'jsMasseges':jlist
    }
    return data
