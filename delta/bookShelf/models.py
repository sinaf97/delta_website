from django.db import models
from dashboard.models import course




class book(models.Model):
    title = models.CharField(max_length=60,null=True,blank = True)
    course = models.ForeignKey(course,max_length=60,null=True,blank = True)
    desc = models.CharField(max_length=512,null=True,blank=True)
