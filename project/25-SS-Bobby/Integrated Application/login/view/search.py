"""
===============================================================================
Search
===============================================================================

Author:
    Ganga Sunil

Functionality:
    This module provides search functionality for students and teachers. 

Vulnerebility:
    It use the raw SQL queries with direct string interpolation, making it vulnerable to SQL Injection attacks. 

"""

from functools import wraps
from django.shortcuts import render
from login.models import Login, Student, Marks, StudentReg, TeacherReg, TimetableEntry, ClassSection, Subject, TeacherAvailability, TimeSlot,StudentReg1,Teacher,Teachers,Answer, Question
from django.db import connection
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