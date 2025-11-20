from django.urls import path
from mainApp import views

urlpatterns = [
    path("",views.home,name='home'),
    path("doctor/",views.doctorDashboard,name='doctorDashboard'),
    path("patient/",views.patientDashboard,name='patientDashboard'),
    path("appointment/",views.addPatientAppoinment,name='appointment'),
    path("confirmAppointment/<int:id>",views.confirmAppointment,name='confirmAppointment'),
    path("editDoctorProfile/",views.editDoctorProfile,name='editDoctorProfile'),
    path("editPatientProfile/",views.editPatientProfile,name='editPatientProfile'),
    path("downloadAppointmentList/",views.downloadAppointmentList,name='downloadAppointmentList'),
    path("cancelAppoinment/<int:id>",views.cancelAppointment,name='cancelAppoinment'),
    path("deleteAppoinment/<int:id>",views.deleteAppointment,name='deleteAppoinment'),
]
