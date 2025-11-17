"""
=============================================================
 Student Application Feature
=============================================================

Author:
    Thoomu Sai Bhargav

Functionality:
    - Public/student-facing page to submit a student application.
    - Prefills some values from latest StudentReg record (if exists).

Security Notes / Potential Vulnerabilities:
    - Make sure StudentApplicationForm validates/cleans all fields.
    - Ensure templates escape user inputs to avoid stored XSS.
=============================================================
"""
from django.shortcuts import render, redirect
from django.contrib import messages

from login.models import StudentApplication, StudentReg
from login.forms import StudentApplicationForm


def student_application_view(request):
    """
    Render and process the student application form.
    """
    prefill_data = {}
    latest_reg = StudentReg.objects.last()  # adjust if needed

    GENDER_DISPLAY = {'M': 'Male', 'F': 'Female', 'O': 'Others'}

    if latest_reg:
        prefill_data = {
            'student_first_name': latest_reg.firstname,
            'student_last_name': latest_reg.lastname,
            'dob': latest_reg.dob,
            'gender': GENDER_DISPLAY.get(latest_reg.gender, latest_reg.gender),
            'student_email': latest_reg.email,
            'classlevel': f'Class {latest_reg.classlevel}',
        }

    if request.method == "POST":
        form = StudentApplicationForm(request.POST)
        if form.is_valid():
            # Save exactly what the form has validated
            data = form.cleaned_data
            StudentApplication.objects.create(
                student_first_name=data['student_first_name'],
                student_last_name=data['student_last_name'],
                dob=data['dob'],
                gender=data['gender'],
                student_email=data['student_email'],
                classlevel=data['classlevel'],
                student_mobile=data['student_mobile'],
                nationality=data['nationality'],
                blood_group=data['blood_group'],

                student_street=data['student_street'],
                student_house=data['student_house'],
                student_city=data['student_city'],
                student_state=data.get('student_state', ''),
                student_postal=data['student_postal'],

                parent_first_name=data['parent_first_name'],
                parent_last_name=data['parent_last_name'],
                parent_email=data['parent_email'],
                parent_mobile=data['parent_mobile'],
                emergency_contact=data['emergency_contact'],

                parent_street=data['parent_street'],
                parent_house=data['parent_house'],
                parent_city=data['parent_city'],
                parent_state=data.get('parent_state', ''),
                parent_postal=data['parent_postal'],

                prev_school_name=data['prev_school_name'],
                prev_class_grade=data['prev_class_grade'],
                tc_number=data['tc_number'],

                prev_school_street=data['prev_school_street'],
                prev_school_house=data['prev_school_house'],
                prev_school_city=data['prev_school_city'],
                prev_school_state=data['prev_school_state'],
                prev_school_postal=data['prev_school_postal']
            )
            messages.success(request, "Student application submitted successfully!")
            return redirect('index')
    else:
        form = StudentApplicationForm(initial=prefill_data)

    return render(request, "login/studentapplication.html", {"form": form})