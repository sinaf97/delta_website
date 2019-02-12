# Create your models here.
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class term(models.Model):
    year = models.DecimalField(max_digits=4,decimal_places=0,null=True)
    season = models.CharField(max_length=10,null=True)
    part = models.DecimalField(max_digits=1,decimal_places=0,null=True)

    def __str__(self):
        return f"{self.year} => {self.season} {self.part}"


class teacher(models.Model):
    #pic = models.ImageField(upload_to='content/pic')
    user = models.OneToOneField(User,null=True,on_delete = models.CASCADE)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class course(models.Model):
    term = models.ForeignKey(term,null=True,on_delete=models.CASCADE,related_name="courses")
    course_name = models.CharField(max_length=128)
    teacher = models.ForeignKey(teacher,null=True,on_delete=models.PROTECT,related_name='courses')
    code = models.CharField(max_length=8,null=True)
    group = models.DecimalField(max_digits=1,null=True,decimal_places=0)
    def __str__(self):
        return f"{self.course_name} - {self.term}"


class student(models.Model):
    user = models.OneToOneField(User,null=True,on_delete = models.CASCADE)
    course = models.ManyToManyField(course,null=True,related_name='students')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class score(models.Model):
    student = models.ForeignKey(student,null=True,default=None,on_delete=models.CASCADE,related_name="scores")
    course = models.ForeignKey(course,null=True,on_delete=models.PROTECT,related_name="scores")
    scorenum = models.DecimalField(max_digits=3,decimal_places=0)

    def __str__(self):
        return f"Score:{self.scorenum} => {self.student} => {self.course}"
