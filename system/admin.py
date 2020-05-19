from django.contrib import admin
from .models import Course, Student, Date, Teacher
# Register your models here.

admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Date)
admin.site.register(Teacher)