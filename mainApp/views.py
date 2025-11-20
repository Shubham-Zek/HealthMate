from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required,user_passes_test
from .forms import AppointmentForm,PatientProfileForm,DoctorProfileForm
from .models import Appointment,DoctorProfile,PatientProfile
from django.shortcuts import get_object_or_404
# Create your views here.

def isDoctor(user):
    return user.groups.filter(name="Doctor")

def isPatient(user):
    return user.groups.filter(name="Patient")

def home(request):
    return render(request,"mainApp/base.html")

@login_required
@user_passes_test(isDoctor)
def doctorDashboard(request):
    filter=request.GET.get("filter","")
    return render(request,"mainApp/doctorDashboard.html",{'filter':filter})

@login_required
@user_passes_test(isPatient)
def patientDashboard(request):
    filter=request.GET.get("filter","")
    return render(request,"mainApp/patientDashboard.html",{'filter':filter})

# @login_required
# @user_passes_test(isPatient)
def addPatientAppoinment(request):
    form=AppointmentForm()
    if request.method!="POST":
        return render(request,'mainApp/addAppointment.html',{'form':form})
    form=AppointmentForm(request.POST)
    if not form.is_valid():
        return render(request,'mainApp/addAppointment.html',{'form':form})
    appointment=form.save(commit=False)
    appointment.patient=request.user.patientprofile
    appointment.save()
    return redirect('patientDashboard')

@login_required
@user_passes_test(isDoctor)
def manageAppointment(request):
    return render(request,'mainApp/manageAppointment.html')

@login_required
@user_passes_test(isDoctor)
def confirmAppointment(request,id):
    appointment=get_object_or_404(Appointment,id=id,doctor=request.user.doctorprofile)
    appointment.status='Confirmed'
    appointment.save()
    return redirect('doctorDashboard')

@login_required
def editDoctorProfile(request):
    form=DoctorProfileForm(instance=request.user.doctorprofile)
    if request.method!="POST":
        return render(request,'mainApp/editProfile.html',{'form':form})
    form=DoctorProfileForm(request.POST, instance=request.user.doctorprofile)
    if not form.is_valid:
        return render(request,'mainApp/editProfile.html',{'form':form})
    form.save()
    return redirect('doctorDashboard')

@login_required
def editPatientProfile(request):
    form=PatientProfileForm(instance=request.user.patientprofile)
    if request.method!="POST":
        return render(request,'mainApp/editProfile.html',{'form':form})
    form=PatientProfileForm(request.POST, instance=request.user.patientprofile)
    if not form.is_valid:
        return render(request,'mainApp/editProfile.html',{'form':form})
    form.save()
    return redirect('patientDashboard')


import csv
@login_required
@user_passes_test(isDoctor)
def downloadAppointmentList(request):
    appointments=Appointment.objects.filter(doctor=request.user.doctorprofile)
    response=HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment; filename="patientList.csv"'

    writer=csv.writer(response)
    writer.writerow(['Patient Name','Email','Age','Gender','Appointment Date','Appointment Time','Status'])

    for appointment in appointments:
        writer.writerow([
            appointment.patient.user.username,
            appointment.patient.user.email,
            appointment.patient.age,
            appointment.patient.gender,
            appointment.date,
            appointment.time,
            appointment.status
        ])
    return response


from django.core.mail import send_mail
from django.conf import settings

@login_required
@user_passes_test(isPatient)
def cancelAppointment(request,id):
    appointment=get_object_or_404(Appointment, id=id,patient=request.user.patientprofile)
    appointment.status='Cancelled'
    appointment.save()

    send_mail(
        subject= "Appointment Cancelled",
        message=f'Hi {appointment.patient.user.username}, your appointment with Dr. {appointment.doctor.user.username} on {appointment.date} at {appointment.time} has been cancelled',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[appointment.patient.user.email],
    )
    return redirect('patientDashboard')


@login_required
@user_passes_test(isPatient)
def deleteAppointment(request,id):
    appointment=get_object_or_404(Appointment,id=id)
    appointment.delete()
    return redirect('patientDashboard')

