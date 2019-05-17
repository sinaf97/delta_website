from django.urls import path
from . import views
from finance.views import show_invoice,tranaction_history

urlpatterns = [
    path(r'',views.default.dashboard,name="dashboard"),
    path(r'settings/',views.default.settings,name="settings"),
    path(r'settings/change_name/',views.default.change_name,name="change_name"),
    path(r'settings/change_pass/',views.default.change_pass,name="change_pass"),
    path(r'settings/change_profile_photo/',views.default.change_profile_photo,name="change_profile_photo"),
    path(r'mail/inbox/',views.default.inbox,name="inbox"),
    path(r'mail/inbox/seen/',views.default.inbox_seen,name="inbox_seen"),
    path(r'mail/compose/',views.default.compose,name="compose"),
    path(r'mail/send/',views.default.mail_send,name="mail_send"),
    path(r'mail/delete/',views.default.mail_delete,name="mail_delete"),
    path(r'mail/reply/<str:username>/',views.default.compose,name="mail_reply"),

    path(r'student_info/',views.studentViews.info,name="s_info"),
    path(r'score/',views.studentViews.studentScore,name="score"),
    path(r'finance/invoice/',show_invoice,name="invoice"),
    path(r'finance/history/',tranaction_history,name="tranaction_history"),
    path(r's_massege/',views.studentViews.s_massege,name="s_massege"),
    path(r'reports/',views.studentViews.reports,name="reports"),

    path(r'teacher_info/',views.teacherViews.info,name="t_info"),
    path(r'courses/',views.teacherViews.courses,name="courses"),
    path(r'courses/submit/',views.teacherViews.add_score,name="add_score"),
    path(r'courses/<str:info>/',views.teacherViews.courseInfo,name="course_info"),

    path(r'add_user/',views.adminViews.add_user,name="add_user"),
    path(r'add_user/submit/',views.adminViews.add_user_submit,name="add_user_submit"),
    path(r'add_user/submit/validate_username/',views.adminViews.validate_username,name="validate_username"),
    path(r'add_term/',views.adminViews.add_term,name="add_term"),
    path(r'add_term/submit/',views.adminViews.add_term_submit,name="add_term_submit"),
    path(r'new_course/',views.adminViews.new_course,name="new_course"),
    path(r'new_course/submit/',views.adminViews.new_course_submit,name="new_course_submit"),
    path(r'course_to_term/',views.adminViews.course_to_term,name="course_to_term"),
    path(r'course_to_term/submit/',views.adminViews.course_to_term_submit,name="course_to_term_submit"),
    path(r'course_to_term/auto_fill/',views.adminViews.auto_fill,name="auto_fill"),
    path(r'students_to_course/',views.adminViews.students_to_course,name="students_to_course"),
    path(r'students_to_course/submit/',views.adminViews.students_to_course_submit,name="students_to_course_submit"),
    path(r'student_to_course/validate_usernames/',views.adminViews.validate_usernames,name="validate_usernames"),
    path(r'student_to_course/get_term_course/',views.adminViews.getTermCourse,name="get_term_course"),
    path(r'get_users/',views.adminViews.get_users,name="get_users"),
    path(r'get_users/ajax/',views.adminViews.get_users_ajax,name="get_users_ajax"),
    path(r'get_courses/',views.adminViews.get_courses,name="get_courses"),
    path(r'get_courses/ajax/',views.adminViews.get_courses_ajax,name="get_courses_ajax"),
    path(r'users/<str:info>/',views.adminViews.get_info,name="get_info"),
    path(r'users/<str:info>/edit_user/',views.adminViews.edit_user,name="edit_user"),
    path(r'users/<str:info>/edit_user/ajax/',views.adminViews.edit_user_ajax,name="edit_user_ajax"),
    path(r'course/<str:info>/',views.adminViews.get_course_info,name="get_course_info"),
    path(r'book_shelf/',views.adminViews.book_shelf,name="book_shelf"),

]