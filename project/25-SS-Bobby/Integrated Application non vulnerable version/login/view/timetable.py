import random
from django.db import models
from login.models import *

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
from login.views import *


@session_required('Admin_login')
def create_timetable(request):
    return render(request, 'login/home.html')

@session_required('Admin_login')
def add_subject(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_subject')
    else:
        form = SubjectForm()
    return render(request, 'login/add_subject.html', {'form': form})

@session_required('Admin_login')
def add_teacher(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_teacher')
    else:
        form = TeacherForm()
    return render(request, 'login/add_teacher.html', {'form': form})


@session_required('Admin_login')
def add_classsection(request):
    if request.method == 'POST':
        form = ClassSectionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_classsection')
    else:
        form = ClassSectionForm()
    return render(request, 'login/add_classsection.html', {'form': form})

@session_required('Admin_login')
def add_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_room')
    else:
        form = RoomForm()
    return render(request, 'login/add_room.html', {'form': form})

@session_required('Admin_login')
def add_timeslot(request):
    if request.method == 'POST':
        form = TimeSlotForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_timeslot')
    else:
        form = TimeSlotForm()
    return render(request, 'login/add_timeslot.html', {'form': form})

@session_required('Admin_login')
def generate_timetable_view(request):
    failures = None
    if request.method == 'POST':
        failures = generate_timetable()
    return render(request, 'login/generate_timetable.html', {'failures': failures})

@session_required('Admin_login')
def admin_timetable_view(request):
    class_id = request.GET.get('class_id')
    subject_id = request.GET.get('subject_id')
    teacher_id = request.GET.get('teacher_id')
    day = request.GET.get('day')

    entries = TimetableEntry.objects.all()

    if class_id:
        entries = entries.filter(class_section_id=class_id)
    if subject_id:
        entries = entries.filter(subject_id=subject_id)
    if teacher_id:
        entries = entries.filter(teacher_id=teacher_id)
    if day:
        entries = entries.filter(timeslot__day=day)

    entries = entries.order_by('class_section', 'timeslot__day', 'timeslot__period')

    context = {
        'entries': entries,
        'classes': ClassSection.objects.all(),
        'subjects': Subject.objects.all(),
        'teachers': TeacherAvailability.objects.all(),
        'days': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
        'selected_class': int(class_id) if class_id else '',
        'selected_subject': int(subject_id) if subject_id else '',
        'selected_teacher': int(teacher_id) if teacher_id else '',
        'selected_day': day or '',
    }
    return render(request, 'login/timetable.html', context)


@session_required('Teacher_login')
def teacher_timetable_view(request):
    username = request.session.get('login_username')
    day = request.GET.get('day')

    try:
        teacher = TeacherAvailability.objects.get(username=username)
    except TeacherAvailability.DoesNotExist:
        return render(request, 'login/Teacher_timetable.html', {
            'entries': [],
            'error': "Teacher not found.",
        })

    entries = TimetableEntry.objects.filter(teacher=teacher)

    if day:
        entries = entries.filter(timeslot__day=day)

    entries = entries.order_by('class_section', 'timeslot__day', 'timeslot__period')

    context = {
        'entries': entries,
        'days': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
        'selected_day': day or '',
    }
    return render(request, 'login/teacher_timetable.html', context)

def generate_timetable():
    TimetableEntry.objects.all().delete()
    slots = list(TimeSlot.objects.all())
    rooms = list(Room.objects.all())
    teachers = list(TeacherAvailability.objects.all())

    teacher_day_load = {(t.id, day): 0 for t in teachers for day, _ in DAYS}
    teacher_week_load = {t.id: 0 for t in teachers}
    failures = []

    for cls in ClassSection.objects.all():
        for subj in cls.subjects.all():
            required = subj.periods_per_week
            assigned = 0
            attempts = 0
            while assigned < required and attempts < required * 20:
                attempts += 1
                slot = random.choice(slots)

                teacher_pool = TeacherAvailability.objects.filter(
                    subjects=subj,
                    class_sections=cls
                ).exclude(unavailable=slot)
                teacher_pool = [t for t in teacher_pool if teacher_day_load[(t.id, slot.day)] < t.max_periods_per_day
                                and teacher_week_load[t.id] < t.max_periods_per_week]
                if not teacher_pool:
                    continue
                teacher = random.choice(teacher_pool)

                if subj.specialized_room:
                    room_pool = [r for r in rooms if r.room_type == subj.specialized_room]
                else:
                    room_pool = [r for r in rooms if r.room_type.lower() == "regular"]

                if not room_pool:
                    continue
                room = random.choice(room_pool)

                if TimetableEntry.objects.filter(timeslot=slot).filter(
                    models.Q(class_section=cls) |
                    models.Q(teacher=teacher) |
                    models.Q(room=room)
                ).exists():
                    continue

                TimetableEntry.objects.create(
                    class_section=cls, subject=subj, teacher=teacher, room=room, timeslot=slot
                )
                assigned += 1
                teacher_day_load[(teacher.id, slot.day)] += 1
                teacher_week_load[teacher.id] += 1

            if assigned < required:
                failures.append((cls.name, subj.name, required - assigned))

    return failures
