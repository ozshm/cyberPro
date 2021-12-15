from django import forms

from .models import User, ChangePwd

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'password',
        ]

class ChangePwdForm(forms.ModelForm):
    class Meta:
        model = ChangePwd
        fields = [
            'existingPassword',
            'newPassword',
        ]
        labels = {
            'existingPassword': 'Existing Password',
            'newPassword': 'New Password',
        }