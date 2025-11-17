"""
=============================================================
 Student Approval Feature (Admin)
=============================================================

Author:
    Thoomu Sai Bhargav

Functionality:
    - Admin lists pending student applications.
    - Admin may approve (creates Student + Login) or reject.

Security Notes / Potential Vulnerabilities:
    - Requires admin session gate via session_required('Admin_login').
    - Ensure passwords are rotated later; initial password is a random token.
=============================================================
"""
import secrets
import string
import random
import hashlib

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from login.models import StudentApplication, Student, Login
from login.views import session_required


def generate_username():
    letters = ''.join(random.choices(string.ascii_uppercase, k=3))
    digits = ''.join(random.choices(string.digits, k=3))
    return letters + digits

def generate_password():
    return secrets.token_urlsafe(8)

def simple_hash(password):
    return hashlib.md5(password.encode()).hexdigest()

@session_required('Admin_login')
def student_approval(request):
    """
    Show pending student applications (by email not already approved).
    """
    approved_emails = set(
        email.strip().lower()
        for email in Login.objects.filter(role='Student').values_list('email', flat=True)
        if email
    )
    all_students = StudentApplication.objects.all()
    pending_students = [s for s in all_students if s.student_email and s.student_email.strip().lower() not in approved_emails]
    return render(request, 'login/student_approval.html', {'students': pending_students})

@session_required('Admin_login')
def approve_student(request, student_id):
    """
    Approve a student application → create Student + Login.
    """
    student = get_object_or_404(StudentApplication, id=student_id)

    if Login.objects.filter(email__iexact=student.student_email, role='Student').exists():
        messages.warning(request, "Student already approved.")
        return redirect('student_approval')

    username = generate_username()
    password = generate_password()

    Student.objects.create(
        username=username,
        student_first_name=student.student_first_name,
        student_last_name=student.student_last_name,
        dob=student.dob,
        gender=student.gender,
        student_email=student.student_email,
        classlevel=student.classlevel,
        student_mobile=student.student_mobile,
        nationality=student.nationality,
        blood_group=student.blood_group,

        student_street=student.student_street,
        student_house=student.student_house,
        student_city=student.student_city,
        student_state=student.student_state,
        student_postal=student.student_postal,

        parent_first_name=student.parent_first_name,
        parent_last_name=student.parent_last_name,
        parent_email=student.parent_email,
        parent_mobile=student.parent_mobile,
        emergency_contact=student.emergency_contact,

        parent_street=student.parent_street,
        parent_house=student.parent_house,
        parent_city=student.parent_city,
        parent_state=student.parent_state,
    )

    Login.objects.create(
        username=username,
        password=password, # NOTE: Plain field in your codebase; ensure you hash later when migrating to Django auth
        role='Student',
        email=student.student_email.strip()
    )

    messages.success(request, "Student approved.")
    return redirect('student_approval')

@session_required('Admin_login')
def reject_student(request, student_id):
    """
    Reject a student application (delete record).
    """
    student = get_object_or_404(StudentApplication, id=student_id)
    student.delete()
    messages.info(request, "Student application rejected.")
    return redirect('student_approval')
