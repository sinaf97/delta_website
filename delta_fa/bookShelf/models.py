from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator


def book_picPath(book,fileName):
    fileName = fileName.split('.')[1]
    return f"books/{book.book_group.group_name}/{book.title}/book pic/{book.title}.{fileName}"

def book_group_picPath(book,fileName):
    fileName = fileName.split('.')[1]
    return f"books/{book.group_name}/group pic/{book.group_name}.{fileName}"

class Book(models.Model):
    title = models.CharField(max_length=60,null=True,blank = True)
    book_group = models.ForeignKey('BookGroup',on_delete=models.CASCADE,null=True)
    authors = models.CharField(max_length=128,null=True,blank=True)
    publish_date = models.ForeignKey('Date',null=True,on_delete=models.PROTECT)
    publish_place = models.CharField(max_length=64,null=True,blank=True)
    level = models.CharField(max_length=32,null=True,blank=True)
    book_pic = models.FileField(upload_to=book_picPath,null=True,default='default/book_pic.jpg')
    description = models.TextField(max_length=512,null=True,blank=True)

    def __str__(self):
        return f"{self.title}"

class Date(models.Model):
    year = models.PositiveIntegerField(null=True)
    month = models.PositiveIntegerField(null=True,validators=[MinValueValidator(1),MaxValueValidator(12)])
    day = models.PositiveIntegerField(null=True,validators=[MinValueValidator(1),MaxValueValidator(30)])

    def __str__(self):
        return f"{self.year}/{self.month}/{self.day}"

class BookGroup(models.Model):
    group_name = models.CharField(max_length=60,null=True,blank = True)
    group_pic  = models.FileField(upload_to=book_group_picPath,null=True,default='default/book_pic.jpg')
    level = models.CharField(max_length=20,null=True,blank=True)
    description = models.TextField(max_length=64,null=True,blank=True)
    def __str__(self):
        return f"{self.group_name}"
