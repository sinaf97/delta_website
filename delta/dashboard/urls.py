from django.urls import path
from . import views

urlpatterns = [
    path('',views.default.dashboard,name="dashboard"),
    path('settings',views.default.settings,name="settings"),
    path('settings/change_name',views.default.change_name,name="change_name"),
    path('settings/change_pass',views.default.change_pass,name="change_pass"),
    path('settings/change_profile_photo',views.default.change_profile_photo,name="change_profile_photo"),

    path('student_info',views.studentViews.info,name="s_info"),
    path('score',views.studentViews.studentScore,name="score"),
    path('s_massege',views.studentViews.s_massege,name="s_massege"),
    path('s_massege/ajax',views.studentViews.s_massege_ajax,name="s_massege_ajax"),
    path('r_massege',views.studentViews.r_massege,name="r_massege"),
    path('reports',views.studentViews.reports,name="reports"),

    path('teacher_info',views.teacherViews.info,name="t_info"),
    path('courses',views.teacherViews.courses,name="courses"),
    path('t_r_massege',views.teacherViews.r_massege,name="t_r_massege"),
    path('courses/submit',views.teacherViews.add_score,name="add_score"),
    path('courses/<str:info>',views.teacherViews.courseInfo,name="course_info"),

    path('add_user',views.adminViews.add_user,name="add_user"),
    path('add_user/submit',views.adminViews.add_user_submit,name="add_user_submit"),
    path('add_user/submit/validate_username',views.adminViews.validate_username,name="validate_username"),
    path('add_term',views.adminViews.add_term,name="add_term"),
    path('add_term/submit',views.adminViews.add_term_submit,name="add_term_submit"),
    path('new_course',views.adminViews.new_course,name="new_course"),
    path('new_course/submit',views.adminViews.new_course_submit,name="new_course_submit"),
    path('course_to_term',views.adminViews.course_to_term,name="course_to_term"),
    path('course_to_term/submit',views.adminViews.course_to_term_submit,name="course_to_term_submit"),
    path('course_to_term/auto_fill',views.adminViews.auto_fill,name="auto_fill"),
    path('students_to_course',views.adminViews.students_to_course,name="students_to_course"),
    path('students_to_course/submit',views.adminViews.students_to_course_submit,name="students_to_course_submit"),
    path('student_to_course/validate_usernames',views.adminViews.validate_usernames,name="validate_usernames"),
    path('student_to_course/get_term_course',views.adminViews.getTermCourse,name="get_term_course"),
    path('get_users',views.adminViews.get_users,name="get_users"),
    path('get_users/ajax',views.adminViews.get_users_ajax,name="get_users_ajax"),
    path('get_courses',views.adminViews.get_courses,name="get_courses"),
    path('get_courses/ajax',views.adminViews.get_courses_ajax,name="get_courses_ajax"),
    path('users/<str:info>',views.adminViews.get_info,name="get_info"),
    path('users/<str:info>/edit_user',views.adminViews.edit_user,name="edit_user"),
    path('users/<str:info>/edit_user/ajax',views.adminViews.edit_user_ajax,name="edit_user_ajax"),
    path('course/<str:info>',views.adminViews.get_course_info,name="get_course_info"),
    path('book_shelf',views.adminViews.book_shelf,name="book_shelf"),

]
