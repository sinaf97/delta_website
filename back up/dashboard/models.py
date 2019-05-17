# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from bookShelf.models import Book


def picPath(user,fileName):
    fileName = fileName.split('.')[1]
    return f"users/{user.role}s/{user.username}/profile pic/{user.username}.{fileName}"
def teacherPicPath(user,fileName):
    fileName = fileName.split('.')[1]
    return f"users/{user.role}s/{user.username}/public pic/{user.username}.{fileName}"

class User(AbstractUser):
    role = models.CharField(max_length=30)
    phone = models.CharField(max_length=12,null=True)
    mobile= models.CharField(max_length=12,null=True)
    idCode = models.CharField(max_length=10,null=True)
    address = models.TextField(max_length=256,null=True)
    pic = models.FileField(upload_to=picPath,null=True,default='default/profile.png')
    # finance = models.OneToOneField('Financial',on_delete = models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# Create your models here.

class Term(models.Model):
    year = models.IntegerField(null=True)
    season = models.CharField(max_length=10,null=True)
    part = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.year} => {self.season} {self.part}"
    def getTermInfo(self):
        return {'year':self.year,'season':self.season,'part':self.part}

class Teacher(models.Model):
    #pic = models.ImageField(upload_to='content/pic')
    user = models.OneToOneField(User,null=True,on_delete = models.CASCADE)
    status = models.BooleanField(default=False)
    certificate = models.CharField(max_length=64,null=True)
    pic = models.FileField(upload_to=teacherPicPath,null=True,default='default/default teacher.jpg')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    def statusConvert(self):
        if(self.status):
            return "true"
        else:
            return "false"
    def getTeacherInfo(self):
        return {'name':self.user.first_name+" "+self.user.last_name,'status':self.statusConvert(),'username':self.user.username}

class Course(models.Model):
    term = models.ForeignKey(Term,null=True,on_delete=models.CASCADE,related_name="courses")
    teacher = models.ForeignKey(Teacher,null=True,on_delete=models.PROTECT,related_name='courses')
    courseInfo = models.ForeignKey('CourseInfo',null=True,on_delete=models.PROTECT,related_name='courses')
    group = models.IntegerField(null=True)
    def __str__(self):
        return f"{self.courseInfo.course_name} - {self.term}"
    def getCourseInfo(self):
        return {'term':self.term.getTermInfo(),'course_name':self.courseInfo.course_name,'teacher':self.teacher.getTeacherInfo(),'code':self.courseInfo.code,'group':self.group}

class CourseInfo(models.Model):
    course_name = models.CharField(max_length=128)
    code = models.CharField(max_length=8,null=True)
    book = models.ForeignKey(Book,null=True,on_delete=models.PROTECT,related_name='courses')
    student_price = models.FloatField(default = 100)
    teacher_price = models.FloatField(default = 100)

    def __str__(self):
        return f"{self.course_name}"

class Student(models.Model):
    user = models.OneToOneField(User,null=True,on_delete = models.CASCADE)
    course = models.ManyToManyField(Course,related_name='students')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    def getStudentInfo(self):
        return {'username':self.user.username,'name':self.__str__()}

class Score(models.Model):
    student = models.ForeignKey(Student,null=True,default=None,on_delete=models.CASCADE,related_name="scores")
    course = models.ForeignKey(Course,null=True,on_delete=models.CASCADE,related_name="scores")
    midScore = models.FloatField(null=True)
    finalScore = models.FloatField(null=True)

    def __str__(self):
        return f"Midterm: {self.midScore} - Final: {self.finalScore} => {self.student} => {self.course}"
    def getScoreInfo(self):
        return {'username':self.student.user.username,'midScore':self.midScore,'finalScore':self.finalScore}

class Massege(models.Model):
    id = models.CharField(max_length=40,null = False,primary_key = True)
    origin =  models.ForeignKey(User,null=True,default=None,on_delete=models.CASCADE,related_name="sent_masseges")
    to =  models.ForeignKey(User,null=True,default=None,on_delete=models.CASCADE,related_name="recieved_masseges")
    seen = models.BooleanField(default = True)
    time_sent = models.TimeField(auto_now_add = True)
    date_sent = models.DateField(auto_now_add = True)
    subject = models.CharField(max_length = 64)
    text = models.TextField(max_length=512,null=True)
