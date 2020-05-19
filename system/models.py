from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Course(models.Model):
    course_name = models.CharField(max_length = 200)
    course_number = models.IntegerField(unique = True)

    def __str__(self):
        return self.course_name.upper()

class Student(models.Model):
    first_name = models.CharField(max_length = 64)
    last_name = models.CharField(max_length = 64)
    prn_number = models.CharField(max_length = 10, unique = True)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    email = models.EmailField(max_length = 254)
    profile_picture = models.ImageField(upload_to = 'profile_picture', default='pp.jpg' )
    
    def __str__(self):
        return self.first_name+' '+self.last_name

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to = 'profile_picture/teacher', default='pp.jpg' )

    

class Date(models.Model):
    reason = models.CharField(max_length=200, null=False, default='Regular Attendance')
    date = models.DateField(auto_now=True, auto_now_add = False)
    prn_numbers = models.ManyToManyField(Student)
    

    def __str__(self):
        return self.reason+' at '+str(self.date)