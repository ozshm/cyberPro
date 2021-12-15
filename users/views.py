from django.shortcuts import render

from .forms import UserForm, ChangePwdForm

from .models import User, ChangePwd
# Create your views here.

def user_create_view(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = UserForm()
    context = {
        'form': form,
        'page_name': 'register',
    }

    return render(request, "users/user_create.html", context)

def user_change_pwd_view(request):
    form = ChangePwdForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = ChangePwdForm()
    context = {
        'form': form,
        'page_name': 'change password',
    }
    return render(request, "users/user_change_pwd.html", context)