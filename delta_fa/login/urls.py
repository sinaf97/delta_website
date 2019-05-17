from django.urls import path
from . import views

urlpatterns = [
    path(r'',views.lin,name="lin"),
    path(r'auth/',views.auth,name="auth"),
]
