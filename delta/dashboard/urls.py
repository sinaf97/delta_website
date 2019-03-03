from django.urls import path
from . import views

urlpatterns = [
    path('',views.dashboard,name="dashboard"),
    path('/score',views.studentScore,name="score"),
    path('/s_messege',views.s_messege,name="s_messege"),
    path('/r_messege',views.r_messege,name="r_messege"),
    path('/reports',views.reports,name="reports"),
    path('/courses',views.courses,name="courses"),
    path('/courses/submit',views.add_score,name="add_score"),
    path(r'/courses/<str:info>',views.courseInfo,name="course_info"),
    path('/add_user',views.add_user,name="add_user"),
    path('/add_user/submit',views.add_user_submit,name="add_user_submit"),
    path('/add_user/submit/validate_username',views.validate_username,name="validate_username"),
    path('/add_term',views.add_term,name="add_term"),
    path('/add_term/submit',views.add_term_submit,name="add_term_submit"),
    path('/new_course',views.new_course,name="new_course"),
    path('/new_course/submit',views.new_course_submit,name="new_course_submit"),
    path('/course_to_term',views.course_to_term,name="course_to_term"),
    path('/course_to_term/submit',views.course_to_term_submit,name="course_to_term_submit"),
    path('/course_to_term/auto_fill',views.auto_fill,name="auto_fill"),
    path('/students_to_course',views.students_to_course,name="students_to_course"),
    path('/students_to_course/submit',views.students_to_course_submit,name="students_to_course_submit"),
    path('/student_to_course/validate_usernames',views.validate_usernames,name="validate_usernames"),
    path('/student_to_course/get_term_course',views.getTermCourse,name="get_term_course"),

]
