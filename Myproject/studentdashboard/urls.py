from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  # For login functionality

app_name = 'studentdashboard'  # Corrected app_name to match the app's namespace

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', views.student_dashboard, name='student_dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='studentdashboard:login'), name='logout'),  # Added logout functionality
    path('student/add/', views.add_student, name='add_student'),
    # path('student/<int:pk>/edit/', views.edit_student, name='edit_student'),  # Added edit student URL
    # path('student/<int:pk>/delete/', views.delete_student, name='delete_student'),  # Added delete student URL
]