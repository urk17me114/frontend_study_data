from functools import wraps
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache

def session_required(role_key):
    def decorator(view_func):
        @wraps(view_func)
        @never_cache
        def _wrapped_view(request, *args, **kwargs):
            if not request.session.get(role_key):
                request.session.flush()
                return redirect('index')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


@never_cache
@session_required('Admin_login')
def admin_dashboard(request):
    functionalities = [
        {'label': 'Manage Timetable', 'url_name': 'create_timetable'},
        {'label': 'Change Password', 'url_name': 'change_password'},
        {'label': 'Search Student', 'url_name': 'search_student'},
        {'label': 'Add Security Question', 'url_name': 'security_question'},
        {'label': 'Profile', 'url_name': 'admin_profile'},
        {'label': 'Approve Students', 'url_name': 'student_approval'},
        {'label': 'Approve Teachers', 'url_name': 'teacher_approval'},
        {'label': 'View Logs', 'url_name': 'view_logs'},
    ]
    return render(request, 'login/dashboard.html', {'role': 'Admin', 'functionalities': functionalities})


@never_cache
@session_required('Teacher_login')
def teacher_dashboard(request):
    functionalities = [
        {'label': 'Add Marks', 'url_name': 'add_marks_step1'},
        {'label': 'Post Question', 'url_name': 'teacher_create_question'},
        {'label': 'My Questions', 'url_name': 'teacher_questions_list'},
        {'label': 'Review Submissions', 'url_name': 'teacher_review_submissions'},  
        {'label': 'Change Password', 'url_name': 'change_password'},
        {'label': 'Add Security Question', 'url_name': 'security_question'},
        {'label': 'View Timetable', 'url_name': 'teacher_timetable'},
        {'label': 'Search Student', 'url_name': 'search_student'},
        {'label': 'Teacher Profile', 'url_name': 'teacher_profile'},
        {'label': 'Make announcement', 'url_name': 'announcement'},
    ]
    return render(request, 'login/dashboard.html', {'role': 'Teacher', 'functionalities': functionalities})


@never_cache
@session_required('Student_login')
def student_dashboard(request):
    functionalities = [
        {'label': 'View Marks', 'url_name': 'view_marks'},
        {'label': 'Questions For Me', 'url_name': 'student_questions_list'},
        {'label': 'My Submissions', 'url_name': 'student_my_submissions'},
        {'label': 'Change Password', 'url_name': 'change_password'},
        {'label': 'Add Security Question', 'url_name': 'security_question'},
        {'label': 'Search Teacher', 'url_name': 'search_teacher'},
        {'label': 'Student Profile', 'url_name': 'student_profile'},
        {'label': 'Q&A forum', 'url_name': 'post_question'},
        {'label': 'View Announcement', 'url_name': 'view_announcement'},
        {'label': 'View timetable', 'url_name': 'student_timetable'},
    ]
    return render(request, 'login/dashboard.html', {'role': 'Student', 'functionalities': functionalities})
