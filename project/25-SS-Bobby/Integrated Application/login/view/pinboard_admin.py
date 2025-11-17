"""
=============================================================
 Admin Pinboard Feature
=============================================================

Author:
    Thoomu Sai Bhargav

Functionality:
    - Admin can create pinboard announcements.
    - Admin can view pinboard list (uses common list renderer).

Security Notes / Potential Vulnerabilities:
    - Ensure templates escape announcement text (avoid stored XSS).
=============================================================
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator

from login.views import session_required
from login.models import Pinboard,Teacher
from login.forms import PinboardForm,Student
from django.views.decorators.cache import never_cache

# Helper function to get display name
def get_display_name(username):
    if username.startswith("ADM"):
        return "Administration Office"
    student = Student.objects.filter(username=username).first()
    if student:
        return f"{student.student_first_name} {student.student_last_name}"
    teacher = Teacher.objects.filter(username=username).first()
    if teacher:
        return f"{teacher.firstname} {teacher.lastname}"
    return username


@never_cache
@session_required('Admin_login')
def create_pinboard(request):
    """
    Admin creates a new pinboard announcement.
    """
    if request.method == 'POST':
        form = PinboardForm(request.POST)
        if form.is_valid():
            pin = form.save(commit=False)
            pin.created_by = request.session.get('login_username')
            pin.save()
            messages.success(request, "Announcement posted successfully.")
            return redirect('pinboard_list_admin')
    else:
        form = PinboardForm()
    return render(request, 'login/create_pinboard.html', {'form': form})

@never_cache
@session_required('Admin_login')
def pinboard_list_admin(request):
    """
    Admin view: list of pinboard announcements (paginated).
    """
    return pinboard_list_common(request, 'Admin')

def pinboard_list_common(request, role):
    announcements = Pinboard.objects.all().order_by('-created_at')
    for ann in announcements:
        ann.display_name = get_display_name(ann.created_by)

    paginator = Paginator(announcements, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Determine dashboard URL for back link
    if role == 'Admin':
        dashboard_url = 'admin'
    elif role == 'Teacher':
        dashboard_url = 'teacher'
    else:
        dashboard_url = 'student'

    return render(request, 'login/pinboard_list.html', {
        'page_obj': page_obj,
        'role': role,
        'dashboard_url': dashboard_url
    })