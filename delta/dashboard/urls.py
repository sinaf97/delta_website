from django.urls import path
from . import views
from finance.views import show_invoice,tranaction_history

urlpatterns = [
    path('',views.default.dashboard,name="dashboard"),
    path('settings',views.default.settings,name="settings"),
    path('settings/change_name',views.default.change_name,name="change_name"),
    path('settings/change_pass',views.default.change_pass,name="change_pass"),
    path('settings/change_profile_photo',views.default.change_profile_photo,name="change_profile_photo"),
    path('mail/inbox',views.default.inbox,name="inbox"),
    path('mail/inbox/seen',views.default.inbox_seen,name="inbox_seen"),
    path('mail/compose',views.default.compose,name="compose"),
    path('mail/send',views.default.mail_send,name="mail_send"),
    path('mail/delete',views.default.mail_delete,name="mail_delete"),
    path('mail/reply/<str:username>',views.default.compose,name="mail_reply"),

    path('student_info',views.studentViews.info,name="s_info"),
    path('score',views.studentViews.studentScore,name="score"),
    path('finance/invoice',show_invoice,name="invoice"),
    path('finance/history',tranaction_history,name="tranaction_history"),
    path('s_massege',views.studentViews.s_massege,name="s_massege"),
    path('reports',views.studentViews.reports,name="reports"),

    path('teacher_info',views.teacherViews.info,name="t_info"),
    path('courses',views.teacherViews.courses,name="courses"),
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
