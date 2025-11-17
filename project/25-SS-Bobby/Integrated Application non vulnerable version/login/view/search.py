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

from login.models import StudentReg
from captcha.fields import CaptchaField
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django import forms
from login.models import Login, Student, Marks, StudentReg, TeacherReg, TimetableEntry, ClassSection, Subject, TeacherAvailability, TimeSlot,StudentReg1,Teacher,Teachers,Answer, Question
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
from login.forms import SearchFormStudent, SearchFormTeacher

def search_student(request):
    results = None
    query = ""
    if request.method == "POST":
        form = SearchFormStudent(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            
            raw_sql = f"SELECT * FROM login_student WHERE student_first_name LIKE '%{query}%'"
            
            with connection.cursor() as cursor:
                cursor.execute(raw_sql)
                columns = [col[0] for col in cursor.description]
                results = [
                    dict(zip(columns, row))
                    for row in cursor.fetchall()
                ]
    else:
        form = SearchFormStudent()
    
    return render(request, "login/search.html", {"form": form, "results": results, "query": query})


def search_teacher(request):
    results = None
    query = ""
    if request.method == "POST":
        form = SearchFormTeacher(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            
            raw_sql = f"SELECT * FROM login_teacher WHERE firstname LIKE '%{query}%'"
            
            with connection.cursor() as cursor:
                cursor.execute(raw_sql)
                columns = [col[0] for col in cursor.description]
                results = [
                    dict(zip(columns, row))
                    for row in cursor.fetchall()
                ]
    else:
        form = SearchFormTeacher()
    
    return render(request, "login/search_teacher.html", {"form": form, "results": results, "query": query})