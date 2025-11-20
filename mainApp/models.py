from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class DoctorProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    specialization=models.CharField(max_length=100)
    experience=models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

GENDER_CHOICES=[
    ('male','Male'),
    ('female','Female'),
    ('others','Others')
]

class PatientProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    age=models.IntegerField(null=True,blank=True)
    gender=models.CharField(choices=GENDER_CHOICES,null=True,blank=True)

    def __str__(self):
        return self.user.username
    
class Appointment(models.Model):
    doctor=models.ForeignKey(DoctorProfile, on_delete=models.CASCADE,related_name='appointments')
    patient=models.ForeignKey(PatientProfile, on_delete=models.CASCADE,related_name='appointments')
    date=models.DateField()
    time=models.TimeField()
    status=models.CharField(max_length=20,default='Pending')