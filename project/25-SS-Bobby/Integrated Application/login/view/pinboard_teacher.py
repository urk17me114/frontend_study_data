"""
=============================================================
 Teacher Pinboard Feature
=============================================================

Author:
    Thoomu Sai Bhargav

Functionality:
    - Teacher can view the pinboard list (read-only).

Security Notes / Potential Vulnerabilities:
    - Only list/reads; ensure templates escape content to avoid XSS.
=============================================================
"""
from django.core.paginator import Paginator
from django.shortcuts import render

from login.views import session_required
from login.models import Pinboard,Student,Teacher
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


# ----------------- COMMON PINBOARD LIST -----------------
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

# ----------------- PINBOARD LIST VIEWS -----------------


@never_cache
@session_required('Teacher_login')
def pinboard_list_teacher(request):
    """
    Teacher view: list of pinboard announcements (paginated).
    """
    return pinboard_list_common(request, 'Teacher')