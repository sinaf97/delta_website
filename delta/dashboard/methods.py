from .models import term , course,score,student,User,teacher



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
    t_courses = request.user.teacher.courses.all()
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
