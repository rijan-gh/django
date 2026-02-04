from django.urls import path
from . import views

app_name = 'studentdashboard'

urlpatterns = [
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
]