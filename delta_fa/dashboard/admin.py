from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Student)
admin.site.register(Score)
admin.site.register(Course)
admin.site.register(Teacher)
admin.site.register(Term)
admin.site.register(CourseInfo)
admin.site.register(Massege)



class UserDisplay(admin.ModelAdmin):
    list_display = ('username','email','first_name','last_name','role','is_staff','is_active')

admin.site.register(User,UserDisplay)
