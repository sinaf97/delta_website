from django.contrib import admin
from .models import student,course,teacher,term,score,User,courseInfo,massege
# Register your models here.

admin.site.register(student)
admin.site.register(score)
admin.site.register(course)
admin.site.register(teacher)
admin.site.register(term)
admin.site.register(courseInfo)
admin.site.register(massege)



class UserDisplay(admin.ModelAdmin):
    list_display = ('username','email','first_name','last_name','role','is_staff','is_active')

admin.site.register(User,UserDisplay)
