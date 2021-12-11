"""cyberpro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from pages.views import login_view, register_view, change_pwd_view, forget_pwd_view, about_view, redirect_to_login_view

from users.views import user_create_view

from clients.views import client_create_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', redirect_to_login_view),
    path('login/', login_view),
    path('register/', user_create_view),
    path('clients/', client_create_view),
    path('change-pwd/', change_pwd_view),
    path('forget-pwd/', forget_pwd_view),
    path('about/', about_view),
    

]
