from django.urls import path
from . import views

urlpatterns = [
    path(r'',views.default.main,name="main"),
    ]
