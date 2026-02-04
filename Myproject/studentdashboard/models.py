from django.db import models

# Create your models here.
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class StudentProfile(models.Model):
    name = models.CharField(max_length=100)
    roll = models.CharField(max_length=20, unique=True)
    program = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class StudentGrade(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='grades')

    # Choices for Semester
    SEM_CHOICES = [
        ('1st', '1st Semester'),
        ('2nd', '2nd Semester'),
        ('3rd', '3rd Semester'),
        ('4th', '4th Semester'),
        ('5th', '5th Semester'),
        ('6th', '6th Semester'),
        ('7th', '7th Semester'),
        ('8th', '8th Semester'),
    ]

    year = models.CharField(max_length=4)
    sem = models.CharField(max_length=10, choices=SEM_CHOICES)
    
    # GPA SCALE: 0.00 to 4.00
    gpa = models.DecimalField(
        max_digits=3, 
        decimal_places=2,
        validators=[MinValueValidator(0.0), MaxValueValidator(4.0)],
        help_text="Enter GPA between 0.0 and 4.0"
    )
    
    status = models.CharField(max_length=10, editable=False) # Editable=False hides it in forms

    def save(self, *args, **kwargs):
        # Professional logic: GPA 2.0 is usually the pass mark
        if self.gpa >= 2.0:
            self.status = "Pass"
        else:
            self.status = "Fail"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.name} | {self.sem} | GPA: {self.gpa}"
    