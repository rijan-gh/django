from django.contrib import admin

# Register your models here.
# from .models import StudentProfile, StudentGrade

# admin.site.register(StudentProfile)
# admin.site.register(StudentGrade)

from django.contrib import admin
from .models import StudentProfile, StudentGrade

# 1. This allows us to edit grades directly inside the Student Profile page
class StudentGradeInline(admin.TabularInline):
    model = StudentGrade
    extra = 1  # Provides one empty row to add a new grade quickly
    # We make status readonly because the model calculates it automatically
    readonly_fields = ('status',) 

# 2. Customize the Student Profile view
@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    # Columns to show in the list view
    list_display = ('roll', 'name', 'program')
    # Add a search bar for name and roll number
    search_fields = ('name', 'roll')
    # Plug in the grades inline
    inlines = [StudentGradeInline]
