from django.shortcuts import render, redirect
from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate,login,logout
from authApp.forms import SignupForm,LoginForm,OtpForm
from mainApp.models import DoctorProfile,PatientProfile
from django.contrib import messages

# Create your views here.


# Signup OTP verification
from django.core.mail import send_mail
from django.conf import settings
import random

def signupView(request):
    form=SignupForm()
    if request.method!='POST':
        return render(request,'authApp/signup.html',{'form':form})
    form=SignupForm(request.POST)
    if not form.is_valid():
        return render(request,'authApp/signup.html',{'form':form})
    
    email=form.cleaned_data['email']
    otp=random.randint(100000,999999)

    # store the otp and user data in session
    request.session['otp']=otp
    request.session['user_data']=form.cleaned_data

    # send OTP to email
    send_mail(
        subject='HealthMate: OTP for Registration',
        message=f'Your OTP is {otp}',
        from_email=None,
        recipient_list=[email],
    )
    return redirect('verifyOtp')

def verifyOtp(request):
    # get data from session
    sessionOtp=request.session.get('otp','')
    userData=request.session.get('user_data','')

    # Create form with email data
    form=OtpForm(initial={'email':userData.get('email','')})

    if request.method!='POST':
        return render(request,'authApp/verifyOtp.html',{'form':form})
    form=OtpForm(request.POST)
    if not form.is_valid():
        return render(request,'authApp/verifyOtp.html',{'form':form})

    enteredOtp=int(form.cleaned_data['otp'])
    if enteredOtp==sessionOtp:
        # create user and profile
        user=User(username=userData['username'],email=userData['email'])
        # password
        user.set_password(userData['password'])
        user.save()
        
        # Assigning user to appropriate Group
        role=userData['role']
        group,created=Group.objects.get_or_create(name=role.capitalize())
        user.groups.add(group)

        # Creating profile based on role
    if role=='doctor':
        DoctorProfile.objects.create(user=user)
    if role=='patient':
        PatientProfile.objects.create(user=user)
    messages.success(request,"Registration Successfull !!!")
    return redirect('login')


def loginView(request):
    form=LoginForm()
    if request.method!="POST":
        return render(request,'authApp/login.html',{'form':form})
    form=LoginForm(request.POST)
    if not form.is_valid():
        return render(request,'authApp/login.html',{'form':form})
    username=form.cleaned_data['username']
    password=form.cleaned_data['password']
    role=form.cleaned_data['role']

    user=authenticate(request,username=username,password=password)
    if not user:      
        form.add_error(None,"Invalid Credentials")
        return render(request,'authApp/login.html',{'form':form})
    if not user.groups.filter(name=role.capitalize()):
        form.add_error(None,f"No such {role} exists.")
        return render(request,'authApp/login.html',{'form':form})
    messages.success(request,"Login Successfull !!!")
    login(request,user)
    if role=='doctor':
        return redirect('doctorDashboard')
    if role =='patient':
        return redirect('patientDashboard')
    
def logoutView(request):
    logout(request)
    return redirect('login')