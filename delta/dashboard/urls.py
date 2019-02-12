from django.urls import path
from . import views

urlpatterns = [
    path('',views.dashboard,name="dashboard"),
    path('/score',views.score,name="score"),
    path('/s_messege',views.s_messege,name="s_messege"),
    path('/r_messege',views.r_messege,name="r_messege"),
    path('/reports',views.reports,name="reports"),
    path('/courses',views.courses,name="courses"),
]
