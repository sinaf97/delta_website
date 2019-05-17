from django.urls import path
from . import views

urlpatterns = [
    path('',views.default.main,name="main"),
    ]
