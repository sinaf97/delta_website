from django.urls import path
from . import views

urlpatterns = [
    path(r'',views.index),
    path(r'register/',views.register),
    path(r'change_lang/',views.change_lang),

]
