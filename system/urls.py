from django.contrib import admin
from django.urls import path
from .views import home, about, login_page, register_page, profile_page, create_student, logout_page, take_attendence, show_attendence, attendance_list,delete_attendance, edit_profile, student_profile, edit_student, student_list, delete_student


urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('login/', login_page, name = 'login'),
    path('register/', register_page, name = 'register'),
    path('logout/', logout_page, name = 'logout'),
    path('profile-page/', profile_page, name = 'profile'),
    path('create-student/', create_student, name = 'create_student'),
    path('take-attendance/', take_attendence, name = 'take_attendence'),
    path('show-attendance/<int:id>/', show_attendence, name = 'show_attendance'), 
    path('attendance-list/', attendance_list, name = 'attendance_list'),
    path('delete-attendance/<int:id>/', delete_attendance, name = 'delete_attendance'),
    path('edit-profile/', edit_profile, name = 'edit_profile'),
    path('student-profile/<int:id>/', student_profile, name = 'student_profile'),
    path('edit-student/<int:id>/', edit_student, name = 'edit_student'),
    path('student-list/', student_list, name = 'student_list'),
    path('delete-student/<int:id>/', delete_student, name = 'delete_student'),
]
