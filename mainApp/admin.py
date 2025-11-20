from django.contrib import admin
from .models import DoctorProfile,PatientProfile,Appointment

# Register your models here.
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display=['id','user','specialization','experience']
    list_display_links=['user']
    
admin.site.register(DoctorProfile,DoctorProfileAdmin)

class PatientProfileAdmin(admin.ModelAdmin):
    list_display=['id','user','age','gender']
    list_display_links=['user']

admin.site.register(PatientProfile,PatientProfileAdmin)

class AppointmentAdmin(admin.ModelAdmin):
    list_display=['id','doctor','patient','date','time','status']

admin.site.register(Appointment,AppointmentAdmin)