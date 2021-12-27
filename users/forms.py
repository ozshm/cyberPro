from django import forms

from .models import ForgotPwd, User, ChangePwd, VerifyCode

class UserForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password_repeat = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    phone_number = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control'}), required=False)

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

class ForgotPwdForm(forms.ModelForm):
    class Meta:
        model = ForgotPwd
        fields = [
            'emailAddress',
        ]
        labels = {
            'emailAddress': 'Email Address',
        }

class VerifyCodeForm(forms.ModelForm):
    class Meta:
        model = VerifyCode
        fields = [
            'resetCode',
        ]
        labels = {
            'resetCode': 'Code',
        }