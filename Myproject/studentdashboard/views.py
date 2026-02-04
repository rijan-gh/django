from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import StudentProfile
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required  # <--- THE FIX
import json

from django.contrib import messages

@login_required  # 1. AUTHENTICATION: Only logged-in users get data
def add_student(request):
    if request.method == "POST":
        # 1. DATA EXTRACTION: Handle both Form Data and JSON
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON"}, status=400)
        else:
            data = request.POST

        name = data.get('name')
        roll = data.get('roll')
        program = data.get('program')

        # 2. VALIDATION
        if not name or not roll:
            if request.headers.get('Accept') == 'application/json':
                return JsonResponse({"error": "Name and Roll are required"}, status=400)
            messages.error(request, "Name and Roll Number are required!")
            return render(request, 'add_student.html')

        # 3. DATABASE OPERATION
        student = StudentProfile.objects.create(
            name=name,
            roll=roll,
            program=program
        )

        # 4. RESPONSE LOGIC (React vs HTML)
        if request.headers.get('Accept') == 'application/json':
            return JsonResponse({
                "message": "Student created successfully",
                "id": student.id
            }, status=201) # 201 Created is the standard for new resources

        messages.success(request, f"Student {name} added!")
        return redirect('studentdashboard:student_dashboard')

    # GET Request: Just show the HTML form
    return render(request, 'add_student.html')

def student_dashboard(request):
    # Fetch Data
    students = StudentProfile.objects.prefetch_related('grades').all()
    
    # 2. JSON API LOGIC: Check if requester wants JSON (API call)
    if request.headers.get('Accept') == 'application/json' or request.GET.get('format') == 'json':
        data = []
        for s in students:
            data.append({
                "roll": s.roll,
                "name": s.name,
                "program": s.program,
                "grades": list(s.grades.values('sem', 'gpa', 'status'))
            })
        # 3. STATUS CODE: Return 200 OK with JSON data
        return JsonResponse({"students": data}, status=200)

    # 4. HTML RESPONSE: Standard browser view
    context = {
        'students': students,
        'student_count': students.count(),
    }
    return render(request, 'dashboard.html', context, status=200)


