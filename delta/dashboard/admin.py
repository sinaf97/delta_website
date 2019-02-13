from django.contrib import admin
from .models import student,course,teacher,term,score,User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.

admin.site.register(student)
admin.site.register(score)
admin.site.register(course)
admin.site.register(teacher)
admin.site.register(term)





class TeacherInline(admin.StackedInline):
    model = teacher
    can_delete = False
    verbose_name_plural = 'teacher'

class StudentInline(admin.StackedInline):
    model = student
    can_delete = False
    verbose_name_plural = 'student'
class UserAdmin(BaseUserAdmin):
    inlines = (StudentInline,TeacherInline)

admin.site.register(User,UserAdmin)
