from .forms import UserForm, ChangePwdForm, ForgotPwdForm, VerifyCodeForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.hashers import make_password

# Create your views here.

def user_create_view(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = User.objects.create_user(
                    form.cleaned_data['username'],
                    form.cleaned_data['email'],
                    form.cleaned_data['password']
                )
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.phone_number = form.cleaned_data['phone_number']
        user.save()
        form = UserForm()
    context = {
        'form': form,
        'page_name': 'register',
    }

    return render(request, "users/user_create.html", context)


def login_request(request):
    # The request method 'POST' indicates
    # that the form was submitted
    if request.method == "POST":
        # Create a form instance with the submitted data
        form = AuthenticationForm(request, data=request.POST)
        # Validate the form
        if form.is_valid():
            # If the form is valid, get the user credenetials
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # Authentication of the user
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user,
                      backend='django.contrib.auth.backends.ModelBackend')
                
                # Redirect to homepage
                # print("login!!!!")
                response = redirect('/clients')
                response.set_cookie("isAuthenticated", "true")
                return response
            else:
               print("error")
        else:
            print("username or password error")
            return HttpResponseRedirect("/login")
    form = AuthenticationForm()
    return render(request=request, template_name="../templates/login.html",
     context={
         "login_form": form,
        })

def user_change_pwd_view(request):
    form = ChangePwdForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = ChangePwdForm()
        return redirect('/done')
    else:
        print('Error')
    context = {
        'form': form,
        'page_name': 'change password',
    }
    return render(request, "users/user_change_pwd.html", context)


def logout_request(request):
    print("sup")
    logout(request)
    return redirect('/')


def generate_hased_code():
    # Random password does not include letters/numbers that are similar, like i,l,I,1,0,o to avoid user confusion
    rand_code = User.objects.make_random_password(length=10, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
    hashed_code = make_password(rand_code, salt=None, hasher='sha1')
    return hashed_code

def forgot_pwd_view(request):
    form = ForgotPwdForm(request.POST or None)
    if form.is_valid():
        
        # TODO: Add email query to the DB to verify user exists
        email = form.cleaned_data.get('email')
        if email is not None:
            hashed_code = generate_hased_code()
            subject = 'Communication LTD Password Resetting'
            html_message = render_to_string('forgot_pwd/password_reset_email', {'hashed_code' : hashed_code})
            plain_message = strip_tags(html_message) 
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [User.email, ]
            send_mail( subject, plain_message, email_from, recipient_list )
    
            return redirect('/sent')
    else:
        print('Error')     
    context = {
        'form': form,
        'title': 'Forgot password?',
        'page_name': 'forgot_pwd',
    }
    return render(request, 'forgot_pwd/password_reset_form.html', context)

def email_sent_view(request):
    context = {
        'title': 'Password resetting email sent',
        'page_name': 'sent',
    }
    return render(request, 'forgot_pwd/password_reset_sent.html', context)

def user_changed_pwd_successfully_view(request):
    context = {
        'title': 'Password changed successfully',
        'page_name': 'done',
    }
    return render(request, 'forgot_pwd/password_reset_complete.html', context)

def verify_code_view(request):
    form = VerifyCodeForm(request.POST or None)
    if form.is_valid():
        code = form.cleaned_data.get('code') 
        # TODO: Add resetting code verification according to generated code 
        # TODO: How will I know which code belongs to which user, according to email? username? need to add a column to the DB?
        
        return redirect('/change-pwd/')
    else:
        print('Error')
    context = {
        'form': form,
        'page_name': 'verify reset code',
    }
    return render(request, "forgot_pwd/password_reset_verify_code.html", context)
