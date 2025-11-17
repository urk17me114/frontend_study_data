"""
=============================================================
 Pinboard Detail & Comments Feature
=============================================================

Author:
    Thoomu Sai Bhargav

Functionality:
    - Show a single pinboard announcement + its comments.
    - Allow Admin/Teacher/Student (logged in) to comment.

Security Notes / Potential Vulnerabilities:
    - User-generated comments can lead to stored XSS if templates do not escape.
    - Ensure forms clean input; do not render raw HTML.
    - VULNERABLE: Comments are saved directly from user input without sanitization.
      Any <script> or HTML tags will execute when page is viewed.
=============================================================
"""
from django.shortcuts import render, redirect, get_object_or_404

from login.models import Pinboard
from login.forms import PinboardCommentForm,Teacher,Student
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
def pinboard_detail(request, pk):
    """
    View details of a pinboard announcement + comments.
    Allows commenting by any logged-in role (based on your session scheme).
    """
    announcement = get_object_or_404(Pinboard, pk=pk)
    announcement.display_name = get_display_name(announcement.created_by)

    comments = announcement.comments.all().order_by('created_at')
    for comment in comments:
        comment.display_name = get_display_name(comment.user)

    if request.method == 'POST':
        form = PinboardCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.announcement = announcement

            # Determine current user from available sessions
            if 'Admin_login' in request.session:
                comment.user = request.session.get('login_username')
            elif 'Teacher_login' in request.session:
                comment.user = request.session.get('login_username')
            elif 'Student_login' in request.session:
                comment.user = request.session.get('login_username')
            else:
                comment.user = 'Anonymous'
            
            # VULNERABLE: Saving raw user input directly
            # This allows Stored XSS if the template doesn't escape it

            comment.save()
            return redirect('pinboard_detail', pk=announcement.pk)
    else:
        form = PinboardCommentForm()

    # Which dashboard “Back” should point to?
    if 'Admin_login' in request.session:
        dashboard_url = 'admin'
    elif 'Teacher_login' in request.session:
        dashboard_url = 'teacher'
    elif 'Student_login' in request.session:
        dashboard_url = 'student'
    else:
        dashboard_url = '/'

    return render(request, 'login/pinboard_detail.html', {
        'announcement': announcement,
        'comments': comments,
        'form': form,
        'dashboard_url': dashboard_url
    })