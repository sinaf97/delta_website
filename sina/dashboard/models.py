# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser





class User(AbstractUser):
    role = models.CharField(max_length=30, blank=True)

# Create your models here.

class term(models.Model):
    year = models.IntegerField(null=True)
    season = models.CharField(max_length=10,null=True)
    part = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.year} => {self.season} {self.part}"
    def getTermInfo(self):
        return {'year':self.year,'season':self.season,'part':self.part}


class teacher(models.Model):
    #pic = models.ImageField(upload_to='content/pic')
    user = models.OneToOneField(User,null=True,on_delete = models.CASCADE)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    def statusConvert(self):
        if(self.status):
            return "true"
        else:
            return "false"
    def getTeacherInfo(self):
        return {'name':self.user.first_name+" "+self.user.last_name,'status':self.statusConvert()}


class course(models.Model):
    term = models.ForeignKey(term,null=True,on_delete=models.CASCADE,related_name="courses")
    course_name = models.CharField(max_length=128)
    teacher = models.ForeignKey(teacher,null=True,on_delete=models.PROTECT,related_name='courses')
    code = models.CharField(max_length=8,null=True)
    group = models.IntegerField(null=True)
    def __str__(self):
        return f"{self.course_name} - {self.term}"
    def getCourseInfo(self):
        return {'term':self.term.getTermInfo(),'course_name':self.course_name,'teacher':self.teacher.getTeacherInfo(),'code':self.code,'group':self.group}


class student(models.Model):
    user = models.OneToOneField(User,null=True,on_delete = models.CASCADE)
    course = models.ManyToManyField(course,related_name='students')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    def getStudentInfo(self):
        return {'username':self.user.username,'name':self.__str__()}

class score(models.Model):
    student = models.ForeignKey(student,null=True,default=None,on_delete=models.CASCADE,related_name="scores")
    course = models.ForeignKey(course,null=True,on_delete=models.PROTECT,related_name="scores")
    midScore = models.FloatField(null=True)
    finalScore = models.FloatField(null=True)

    def __str__(self):
        return f"Midterm: {self.midScore} - Final: {self.finalScore} => {self.student} => {self.course}"
    def getScoreInfo(self):
        return {'username':self.student.user.username,'midScore':self.midScore,'finalScore':self.finalScore}
