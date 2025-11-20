from django import forms

# Importing the User model for authentication
from django.contrib.auth.models import User

ROLE_CHOICES =[
    ('doctor','Doctor'),
    ('patient','Patient')
]

class SignupForm(forms.ModelForm):
    role= forms.ChoiceField(choices=ROLE_CHOICES)
    password=forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=['username','email','password']

class LoginForm(forms.Form):
    username=forms.CharField(max_length=100)
    password=forms.CharField(widget=forms.PasswordInput)
    role= forms.ChoiceField(choices=ROLE_CHOICES)

class OtpForm(forms.Form):
    email=forms.CharField(widget=forms.HiddenInput)
    otp=forms.CharField(max_length=6,label="OTP")
