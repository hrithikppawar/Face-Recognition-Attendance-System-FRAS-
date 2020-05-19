from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Student, Teacher

class StudentModelForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'prn_number', 'course', 'email', 'profile_picture']

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
        
class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'
        exclude = ['user']

class StudentEditForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'prn_number', 'course', 'email']