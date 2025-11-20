from django.urls import path
from authApp import views


urlpatterns = [
    path('signup/',views.signupView,name='signup'),
    path('login/',views.loginView,name='login'),
    path('logout/',views.logoutView,name='logout'),
    path('otp/',views.verifyOtp,name='verifyOtp'),
]
