from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator


def book_picPath(book,fileName):
    fileName = fileName.split('.')[1]
    return f"books/{book.book_family_name}/{book.title}/book pic/{book.title}.{fileName}"

class book(models.Model):
    title = models.CharField(max_length=60,null=True,blank = True)
    book_family_name = models.CharField(max_length=60,null=True,blank = True)
    authors = models.CharField(max_length=128,null=True,blank=True)
    publish_date = models.ForeignKey('date',null=True,on_delete=models.PROTECT)
    publish_place = models.CharField(max_length=64,null=True,blank=True)
    level = models.CharField(max_length=32,null=True,blank=True)
    book_pic = models.FileField(upload_to=book_picPath,null=True,default='default/book_pic.jpg')
    description = models.TextField(max_length=512,null=True,blank=True)

class date(models.Model):
    year = models.PositiveIntegerField(null=True)
    month = models.PositiveIntegerField(null=True,validators=[MinValueValidator(1),MaxValueValidator(12)])
    day = models.PositiveIntegerField(null=True,validators=[MinValueValidator(1),MaxValueValidator(30)])
