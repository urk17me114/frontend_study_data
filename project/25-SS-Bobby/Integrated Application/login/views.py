import random
import string
import secrets
import pycountry
import os
import logging
from functools import wraps
import random
import string
import secrets
import time
import logging
import re

from .models import StudentReg
from captcha.fields import CaptchaField
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django import forms
from .models import Login, Student, Marks, StudentReg, TeacherReg, TimetableEntry, ClassSection, Subject, TeacherAvailability, TimeSlot, StudentReg1, Teacher, Teachers, Answer, Question, Login2
from django.contrib.auth import logout as django_logout
from .models import StudentApplication
from django.views.decorators.cache import never_cache
from functools import wraps
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from django.core.cache import cache  # built-in Django cache
from django.http import JsonResponse
from captcha.models import CaptchaStore
from django.core.cache import cache
from django.urls import reverse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.safestring import mark_safe
from django.db import connection
from django.db import transaction
from django.core.exceptions import ValidationError
from django.http import FileResponse, Http404
from django.shortcuts import render, redirect
from .forms import SubjectForm, TeacherForm, ClassSectionForm, RoomForm, TimeSlotForm, EnterStudentMarksForm, SelectClassSubjectForm,  SecurityQuestionForm, ResetPasswordForm, SecurityAnswerForm, ForgotPasswordForm, ChangePasswordForm
from .models import TimetableEntry
from django.views.decorators.cache import never_cache
import hashlib
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django import forms
from .models import Pinboard, PinboardComment




# new ones
from .forms import StudentRegistration, TeacherRegistration, QuestionForm, TeacherAnnouncementForm
from .view.validate_captcha_manual import validate_captcha_manual
from .view.announcement import announcement




CAPTCHA_REUSE_LIMIT = 10
CAPTCHA_TIME_WINDOW = 20  
FLAG = "FLAG{captcha_reuse_detected}"

# --------- Forms ----------

class NewLoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    

    
class FeedbackForm(forms.Form):
    username = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
   


class NewRegistrationForm(forms.Form):
    firstname = forms.CharField(label="Firstname", max_length=50)
    lastname = forms.CharField(label="Lastname", max_length=50)
    email = forms.EmailField(label="Email")
    ROLE_CHOICES = [
        ('Student', 'STUDENT'),
        ('Teacher', 'TEACHER'),
        ('Admin', 'ADMIN'),
    ]
    role = forms.ChoiceField(label="Role", choices=ROLE_CHOICES)


    
   

class MarksForm(forms.Form):
    student_username = forms.CharField(max_length=6)
    subject = forms.CharField(max_length=100)
    marks = forms.IntegerField()




# --------- Helper Functions ----------
def generate_username():
    letters = ''.join(random.choices(string.ascii_uppercase, k=3))
    digits = ''.join(random.choices(string.digits, k=3))
    return letters + digits

def generate_password():
    return secrets.token_urlsafe(8)

def simple_hash(password):
    return hashlib.md5(password.encode()).hexdigest()


# --------- Session check decorator ----------
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


# --------- Views ----------

   

@session_required('Admin_login')
def registration(request):
    if request.method == "POST":
        form = NewRegistrationForm(request.POST)
        if form.is_valid():
            firstname = form.cleaned_data['firstname']
            lastname = form.cleaned_data['lastname']
            email = form.cleaned_data['email']
            role = form.cleaned_data['role']
            password = 'password'

            while True:
                username = generate_username()
                if not Student.objects.filter(username=username).exists():
                    break

            Student.objects.create(
                username=username,
                firstname=firstname,
                lastname=lastname,
                email=email
            )

            Login.objects.create(
                username=username,
                password=password,
                role=role
            )

            messages.success(request, f"{role} registered. Username: {username}, Password: {password}")
            return redirect('registration')
    else:
        form = NewRegistrationForm()

    return render(request, "login/registration.html", {"form": form})


@session_required('Admin_login')
def admin(request):
    return render(request, 'login/admin.html')


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

