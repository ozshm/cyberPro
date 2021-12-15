from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.

def redirect_to_login_view(request, *args, **kwargs):
    response = redirect('/login')
    response.set_cookie('isSecure', 'true')
    return response

def login_view(request, *args, **kwargs):
    # if request.COOKIES['isSecure'] == 'secure':
    #     print("in login page, we are secure!")
    isSecure = request.COOKIES['isSecure'] == 'true'
    my_context = {
        'title': 'welcome test',
        'page_name': 'login',
        'isSecure' : isSecure,
    }
    return render(request, 'login.html', my_context)

def register_view(request, *args, **kwargs):
    my_context = {
        'title': 'register',
        'page_name': 'register',
    }
    return render(request, 'register.html', my_context)   

def change_pwd_view(request, *args, **kwargs):
    my_context = {
        'title': 'change password',
        'page_name': 'change_pwd',
    }
    return render(request, 'change_pwd.html', my_context)

def forget_pwd_view(request, *args, **kwargs):
    my_context = {
        'title': 'forget password',
        'page_name': 'forget_pwd',
    }
    return render(request, 'forget_pwd.html', my_context)

def about_view(request, *args, **kwargs):
    my_context = {
        'title': 'about',
        'page_name': 'about',
    }
    return render(request, 'about.html', my_context)
