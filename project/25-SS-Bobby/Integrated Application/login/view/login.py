"""
===============================================================================
Login page
===============================================================================
Author:
    Arundas Mohandas
Functionality:
    Login authentication with logging of successful and failed login attempts.
    Proper role-based redirection after login.
    Logout functionality that clears session data.

"""
import os
import logging
#from functools import wraps
import logging
from django.shortcuts import render, redirect
from django.http import HttpResponse
from login.models import Login 
#from django.contrib.auth import logout as django_logout
from django.shortcuts import render, redirect
from login.forms import NewLoginForm
#from django.contrib.auth.hashers import check_password
from login.views import simple_hash 
from .error_views import custom_page_not_found_view, custom_permission_denied_view


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
base_dir = os.path.dirname(os.path.abspath(__file__))
logs_dir = os.path.join(base_dir, 'logs')
os.makedirs(logs_dir, exist_ok=True)
log_file_path = os.path.join(logs_dir, 'login_activity.log')
file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

if not logger.hasHandlers():
    logger.addHandler(file_handler)

def view_logs(request):
    if request.GET.get('admin') == '1':
        return serve_log_file("Login Logs")
    else: 
        username = request.session.get('login_username', '')

        user = Login.objects.get(username=username)
        user_role = user.role.strip().lower()

        if user_role == 'admin' :
            return serve_log_file("Login Logs")

    raise custom_permission_denied_view("You are not allowed to see this.")


def serve_log_file(source):
    log_path = os.path.join(os.path.dirname(__file__), './logs', 'login_activity.log')
    if not os.path.exists(log_path):
        raise custom_page_not_found_view("Log file not found.")

    with open(log_path, 'r') as file:
        content = file.read()
    return HttpResponse(f"<h3>{source}</h3><pre>{content}</pre>")


def index(request):
    if request.method == "POST":
        form = NewLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username'].strip()
            password = form.cleaned_data['password'].strip()
            try:
                login = Login.objects.get(username=username)
                if simple_hash(password) == login.password:
                    request.session.flush()
                    request.session[f'{login.role}_login'] = True
                    request.session['login_username'] = username
                    request.session['current_role'] = login.role

                    logger.info(f"User '{username}' logged in successfully as '{login.role}'")

                    if login.role == 'Admin':
                        return redirect('admin')
                    elif login.role == 'Teacher':
                        return redirect('teacher')
                    elif login.role == 'Student':
                        return redirect('student')
                else:
                    logger.warning(f"Failed login attempt for user '{username}': Incorrect password")
                    form.add_error(None, 'Incorrect password')
            except Login.DoesNotExist:
                logger.warning(f"Failed login attempt: Username '{username}' not found")
                form.add_error(None, 'Invalid credentials')
    else:
        form = NewLoginForm() 

    return render(request, "login/login.html", {"form": form})

def logout_view(request):
    request.session.flush()
    return redirect('index')
