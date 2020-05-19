from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import StudentModelForm, SignUpForm, TeacherForm, StudentEditForm
from .models import *
from .identification import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return render(request, 'system/home.html')

def about(request):
    return render(request, 'system/about.html')

def login_page(request):
    if request.user.is_authenticated:
        return redirect('profile')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('profile')
            else:
                messages.info(request, 'Username OR Password is incorrect. Please check again!!!')
        context = {}
        return render(request, 'system/login_page.html', context)

def register_page(request):
    if request.user.is_authenticated:
        return redirect('profile')
    else:
        form = SignUpForm()
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Hi '+user+', account has been created')
                return redirect('login')
        context = {'form':form}
        return render(request, 'system/register_page.html', context)

def logout_page(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
def profile_page(request):
    return render(request, 'system/profile_page.html')

@login_required(login_url='login')
def edit_profile(request):
    teacher = request.user.teacher
    form = TeacherForm(instance=teacher)

    if request.method == 'POST':
        form = TeacherForm(request.POST, request.FILES, instance=teacher)
        if form.is_valid():
            form.save()
        return redirect('profile')
    context = {
        'form': form
    }
    return render(request, 'system/edit_profile.html', context)

@login_required(login_url='login')
def create_student(request):
    form = StudentModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        form = StudentModelForm()

    context = {'form':form}
    return render(request, 'system/create_student.html', context)

@login_required(login_url='login')
def edit_student(request, id):
    obj = Student.objects.get(id=id)
    form = StudentEditForm(instance=obj)

    if request.method == 'POST':
        form = StudentEditForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('student_profile', id)
    context = { 'form':form }
    return render(request, 'system/edit_student.html', context)

@login_required(login_url='login')
def take_attendence(request):
    
    if request.method == 'POST':
        reason = request.POST.get('reason')
        date_obj = Date(reason=reason.title())
        date_obj.save()
        #try:
        attendance = start_detection()
        #except ValueError:
        #    raise Http404("Add Students First")
        prn_numbers = list(attendance.keys())
        time = list(attendance.values())
        for prn_number in prn_numbers:
            student = Student.objects.get(prn_number = int(prn_number))
            date_obj.prn_numbers.add(student)
        id = date_obj.id
        return redirect('show_attendance', id=id)

    
    context = {}
    return render(request, 'system/take_attendence.html', context)

@login_required(login_url='login')
def attendance_list(request):
    if request.method == 'POST':
        date_ = request.POST.get('date')
        obj = Date.objects.filter(date=date_)
        context = {
            'object': obj
        }
        return render(request, 'system/attendance_list.html', context)    
    obj = Date.objects.all()
    context = {
        'object': obj
    }
    return render(request, 'system/attendance_list.html', context)

@login_required(login_url='login')
def show_attendence(request, id):
    obj = Date.objects.get(id=id)
    context={
        'object': obj
    }
    return render(request, 'system/show_attendance.html', context)

@login_required(login_url='login')
def delete_attendance(request, id):
    obj = Date.objects.get(id=id)
    if request.method == 'POST':
        obj.delete()
        return redirect('attendance_list')
    context={
        'object':obj
    }
    return render(request, 'system/delete_attendance.html', context)

@login_required(login_url='login')
def student_profile(request, id):
    obj = Student.objects.get(id=id)
    attendance = obj.date_set.all()
    if request.method == 'POST':
        reason = request.POST.get('reason')
        attendance = obj.date_set.filter(reason = reason.title())
        context = {
            'object': obj,
            'attendance': attendance
        }
        return render(request, 'system/student_profile.html', context)

    context = {
        'object': obj,
        'attendance': attendance
    }
    return render(request, 'system/student_profile.html', context)


@login_required(login_url='login')
def student_list(request):
    if request.method == 'POST':
        prn = request.POST.get('prn')
        obj = Student.objects.filter(prn_number=prn)
        context = {
            'object': obj
        }
        return render(request, 'system/student_list.html', context)    
    obj = Student.objects.all()
    context = {
        'object': obj
    }
    return render(request, 'system/student_list.html', context)


@login_required(login_url='login')
def delete_student(request, id):
    obj = Student.objects.get(id=id)
    if request.method == 'POST':
        obj.delete()
        return redirect('student_list')
    context={
        'object':obj
    }
    return render(request, 'system/delete_student.html', context)