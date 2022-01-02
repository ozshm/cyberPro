from .forms import UserForm, ChangePwdForm, ForgotPwdForm, VerifyCodeForm, ResetPwdForm
#from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.hashers import make_password

from .models import UsersData

import os
import json
import hashlib
import random

# Create your views here. 
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_user_create_requierments(path_to_req):
    with open(os.path.join(BASE_DIR, path_to_req)) as file:
        data = json.load(file)
    return data

def is_valid_password(password):
    count_digit = sum(c.isdigit() for c in password)
    count_alpha = sum(c.isalpha() for c in password)
    count_lower = sum(c.islower() for c in password)
    count_upper = sum(c.isupper() for c in password)
    count_special_char = 0
    req = load_user_create_requierments("cyberpro/pass_req.json")
    for special_char in req['password_content']['special_characters']:
        count_special_char += password.count(special_char)

    if req['min_length'] == len(password):
        return False
    if count_digit < req['password_content']['min_length_digit']:
        return False
    if count_alpha < req['password_content']['min_length_alpha']:
        return False
    if count_lower < req['password_content']['min_length_lower']:
        return False
    if count_upper < req['password_content']['min_length_upper']:
        return False
    if count_special_char < req['password_content']['min_length_special']:
        return False
    return True

def is_difference_password(password, password_repeat):
    return password == password_repeat
 
def user_create_view(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        if not is_valid_password(form.cleaned_data['password']):
            messages.info(request, "The password you entered does not meet the requirements, please try again.")
            return HttpResponseRedirect('/register/')
        if not is_difference_password(form.cleaned_data['password'], form.cleaned_data['password_repeat']):
            messages.info(request, "The passwords do not match, please try again.")
            return HttpResponseRedirect('/register/')
        user = UsersData.objects.create_user(
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
                response = redirect('/clients')
                response.set_cookie("isAuthenticated", "true")
                return response
            return HttpResponseRedirect("/login")
    form = AuthenticationForm()
    return render(request=request, template_name="../templates/login.html",
     context={
         "login_form": form,
         "page_name": "login",
        })

def user_change_pwd_view(request):
    form = ChangePwdForm(request.POST or None)
    context = {
        'form': form,
        'page_name': 'change_pwd',
    }
    if form.is_valid():
        if not is_difference_password(form.cleaned_data['new_password'], form.cleaned_data['verify_password']):
            messages.info(request, "The passwords do not match, please try again.")
            return render(request, "users/user_change_pwd.html", context = context)
        if not is_valid_password(form.cleaned_data['new_password']):
            messages.info(request, "The password you entered does not meet the requirements, please try again.")
            return render(request, "users/user_change_pwd.html", context = context)
        u = UsersData.objects.get(username = request.user)
        if(u is not None):
            if(u.check_password(form.cleaned_data['existing_password'])):
                u.set_password(form.cleaned_data['new_password'])
                u.save()
                return redirect('/change-pwd/done')
            else:
                messages.info(request, "The exising password is not correct, please try again.")
                return render(request, "users/user_change_pwd.html", context = context)
        else:
            messages.info(request, "There was an error, please try again.")
            return render(request, "users/user_change_pwd.html", context = context)
    return render(request, "users/user_change_pwd.html", context = context)


def logout_request(request):
    logout(request)
    return redirect('/')


def forgot_pwd_view(request):
    form = ForgotPwdForm(request.POST or None)
    if form.is_valid():
        email_user = form.cleaned_data.get('email_address')
        found_user = UsersData.objects.filter(email = email_user)
        if found_user.exists():
            hashed_code = hashlib.sha1(str(random.getrandbits(10)).encode('utf-8')).hexdigest()
            subject = 'Communication LTD Password Resetting'
            html_message = render_to_string('forgot_pwd/password_reset_email.html', 
            {
                'hashed_code' : hashed_code,
                'protocol' : 'http',
                'domain' : '127.0.0.1:8000',
                'url' : '/verify-code',
            })
            plain_message = strip_tags(html_message) 
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email_user, ]
            send_mail( subject, plain_message, email_from, recipient_list )
            # Saving hashed_code to the user's db record for authentication
            found_user = UsersData.objects.get(email = email_user)
            found_user.resetCode = hashed_code
            found_user.save()
        # Redirect to /sent even if no user was found so hackers will not know if the user exists
        return redirect('./sent')   
    context = {
        'form': form,
        'title': 'Forgot password?',
        'page_name': 'forgot_pwd',
    }
    return render(request, 'forgot_pwd/password_reset_form.html', context = context)

def email_sent_view(request):
    context = {
        'title': 'Password resetting email sent',
        'page_name': 'sent',
    }
    return render(request, 'forgot_pwd/password_reset_sent.html', context = context)

def user_changed_pwd_successfully_view(request):
    context = {
        'title': 'Password changed successfully',
        'page_name': 'done',
    }
    return render(request, 'forgot_pwd/password_reset_complete.html', context = context)

def verify_code_view(request):
    form = VerifyCodeForm(request.POST or None)
    if form.is_valid():
        input_username = form.cleaned_data.get('username')
        input_code = form.cleaned_data.get('reset_code')
        found_user = UsersData.objects.filter(username = input_username, resetCode = input_code)
        if found_user.exists():
            login(request, found_user[0],
                      backend='django.contrib.auth.backends.ModelBackend')
            response = redirect('/reset-pwd/')
            response.set_cookie("isAuthenticated", "true")
            found_user = UsersData.objects.get(username = input_username)
            found_user.resetCode = None
            found_user.save() 
            return response
        else:
            form = VerifyCodeForm()
            context = {
            'form': form,
            'page_name': 'verify reset code',
            }
            return render(request, "forgot_pwd/password_reset_verify_code.html", context = context)
    context = {
        'form': form,
        'page_name': 'verify reset code',
    }
    return render(request, "forgot_pwd/password_reset_verify_code.html", context = context)

def reset_pwd_view(request):
    form = ResetPwdForm(request.POST or None)
    if form.is_valid():
        if not is_difference_password(form.cleaned_data['new_password'], form.cleaned_data['verify_password']):
            messages.info(request, "The passwords not match, please try again.")
            context = {
            'form': form,
            'page_name': 'reset password',
            }
            return render(request, "users/user_reset_pwd.html", context)
        if not is_valid_password(form.cleaned_data['new_password']):
            messages.info(request, "The password you entered does not meet the requirements, please try again.")
            context = {
            'form': form,
            'page_name': 'reset password',
            }
            return render(request, "users/user_reset_pwd.html", context)
        u = UsersData.objects.get(username = request.user)
        if(u is not None):
            u.set_password(form.cleaned_data['new_password'])
            u.save()
            return redirect('/change-pwd/done')
        else:
            context = {
                'form': form,
                'page_name': 'reset password',
            }
            return render(request, "users/user_reset_pwd.html", context = context)
    else:
        context = {
            'form': form,
            'page_name': 'reset password',
        }
        return render(request, "users/user_reset_pwd.html", context = context)