"""
=============================================================
 Teacher Approval Feature (Admin)
=============================================================

Author:
    Thoomu Sai Bhargav

Functionality:
    - Admin lists pending teacher registrations (TeacherReg).
    - Admin may approve (creates Teacher + Login) or reject.

Security Notes / Potential Vulnerabilities:
    - Requires admin session gate.
    - File fields (documents) must be stored and served safely.
=============================================================
"""
import secrets
import string
import random
import hashlib

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from login.models import TeacherReg, Teacher, Login
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
def teacher_approval(request):
    """
    List teacher registrations not yet approved (by email).
    """
    approved_emails = set(
        email.strip().lower()
        for email in Login.objects.filter(role='Teacher').values_list('email', flat=True)
        if email
    )
    all_teachers = TeacherReg.objects.all()
    pending_teachers = [t for t in all_teachers if t.email and t.email.strip().lower() not in approved_emails]
    return render(request, 'login/teacher_approval.html', {'teachers': pending_teachers})


@session_required('Admin_login')
def approve_teacher(request, teacher_id):
    """
    Approve a teacher registration → create Teacher + Login.
    """
    teacher = get_object_or_404(TeacherReg, id=teacher_id)

    if Login.objects.filter(email__iexact=teacher.email, role='Teacher').exists():
        messages.warning(request, "Teacher already approved.")
        return redirect('teacher_approval')

    username = generate_username()
    password = generate_password()

    # Create entry in Teacher table
    Teacher.objects.create(
        username=username,
        firstname=teacher.firstname,
        lastname=teacher.lastname,
        dob=teacher.dob,
        gender=teacher.gender,
        email=teacher.email,
        document=teacher.document # assumes FileField already uploaded during registration
    )

    # Create login entry
    Login.objects.create(
        username=username,
        password=password,
        role='Teacher',
        email=teacher.email.strip()
    )

    messages.success(request, "Teacher approved.")
    return redirect('teacher_approval')


@session_required('Admin_login')
def reject_teacher(request, teacher_id):
    """
    Reject a teacher registration (delete record).
    """
    teacher = get_object_or_404(TeacherReg, id=teacher_id)
    teacher.delete()
    messages.info(request, "Teacher registration rejected.")
    return redirect('teacher_approval')