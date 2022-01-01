from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.

def redirect_to_login_view(request, *args, **kwargs):
    response = redirect('/login')
    response.set_cookie('isSecure', "true")
    response.set_cookie('isAuthenticated', "false")
    return response

# def login_view(request, *args, **kwargs):
#     # if request.COOKIES['isSecure'] == 'secure':
#     #     print("in login page, we are secure!")
#     my_context = {
#         'title': 'welcome test',
#         'page_name': 'login',
#     }
#     return render(request, 'login.html', my_context)



def about_view(request, *args, **kwargs):
    my_context = {
        'title': 'about',
        'page_name': 'about',
    }
    return render(request, 'about.html', my_context)
