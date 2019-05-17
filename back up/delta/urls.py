"""delta URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404,handler500
from errors import views as error_views

urlpatterns = [
    path('',include('home.urls')),
    path('login',include('login.urls')),
    path('logout',include('logout.urls')),
    path('dashboard/',include('dashboard.urls')),
    path('book_shelf',include('bookShelf.urls')),
    path('finance/',include('finance.urls')),
    path('register',include('home.urls')),
    path(r'error/', include('errors.urls')),
    path('admin/', admin.site.urls),
    path('test',include('home.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()

handler404 = error_views.notfound_404
handler500 = error_views.serverfailure