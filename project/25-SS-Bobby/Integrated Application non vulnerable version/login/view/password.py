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

from login.models import StudentReg
from captcha.fields import CaptchaField
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django import forms
from login.models import Login, Student, Marks, StudentReg, TeacherReg, TimetableEntry, ClassSection, Subject, TeacherAvailability, TimeSlot, StudentReg1, Teacher, Teachers, Answer, Question, Login2
from django.contrib.auth import logout as django_logout
from login.models import StudentApplication
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
from login.forms import SubjectForm, TeacherForm, ClassSectionForm, RoomForm, TimeSlotForm, EnterStudentMarksForm, SelectClassSubjectForm,  SecurityQuestionForm, ResetPasswordForm, SecurityAnswerForm, ForgotPasswordForm, ChangePasswordForm
from login.models import TimetableEntry
from django.views.decorators.cache import never_cache
import hashlib
from login.views import simple_hash




def change_password(request):
    username = request.session.get('login_username')
    role = request.session.get('current_role')

    if not username or not role:
        request.session.flush()
        return redirect('index')

    if request.method == "POST":
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']

            try:
                user = Login.objects.get(username=username)
                if simple_hash(old_password) != user.password:
                    form.add_error('old_password', 'Old password is incorrect.')
                elif new_password != confirm_password:
                    form.add_error('confirm_password', 'New passwords do not match.')
                else:
                    user.password = simple_hash(new_password)
                    user.save()
                    data = Login2.objects.get(username=username)
                    data.password = new_password
                    data.save()
                    messages.success(request, "Password changed successfully.")
                    return redirect(f'{role.lower()}')
            except Login.DoesNotExist:
                request.session.flush()
                return redirect('index')
    else:
        form = ChangePasswordForm()

    return render(request, 'login/change_password.html', {'form': form})

def security_question(request):
    username = request.session.get('login_username')
    if not username:
        return redirect('index')

    try:
        user = Login.objects.get(username=username)
    except Login.DoesNotExist:
        return redirect('index')

    if request.method == "POST":
        form = SecurityQuestionForm(request.POST)
        if form.is_valid():
            user.security_question = form.cleaned_data['security_question']
            user.security_answer = form.cleaned_data['security_answer']
            user.save()
            messages.success(request, "Security question updated successfully.")
            return redirect(f"{user.role.lower()}")
    else:
        form = SecurityQuestionForm()

    return render(request, "login/security_question.html", {"form": form})
