from django.urls import path
from . import views

urlpatterns = [
    path('',views.lin,name="lin"),
    path('auth',views.auth,name="auth"),
]
