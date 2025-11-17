"""
===============================================================================
Marks Management 
===============================================================================

Author:
    Ganga Sunil
    Arundas Mohandas

Functionality:
    Teacher can add marks for the students
    Student can view their marks

Vulnerebility:
    Students can view other students marks.  
=============================================================================== 
"""

from functools import wraps
from django.shortcuts import render, redirect
from django.contrib import messages
from login.models import  Student, Marks, ClassSection, Subject, TeacherAvailability
from django.contrib.auth import logout as django_logout
from django.views.decorators.cache import never_cache
from functools import wraps
from django.core.cache import cache  
from django.http import JsonResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from login.forms import  EnterStudentMarksForm, SelectClassSubjectForm
from django.views.decorators.cache import never_cache
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse


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





@session_required('Teacher_login')
def add_marks_step1(request):
    username = request.session.get('login_username')
    teacher = get_object_or_404(TeacherAvailability, username=username)

    if request.method == 'POST':
        form = SelectClassSubjectForm(teacher, request.POST)
        if form.is_valid():
            request.session['selected_class_section_id'] = form.cleaned_data['class_section'].id
            request.session['selected_subject_id'] = form.cleaned_data['subject'].id
            request.session['total_marks'] = form.cleaned_data['total_marks']
            request.session['exam_type'] = form.cleaned_data['exam_type']
            request.session['exam_date'] = str(form.cleaned_data['exam_date'])  # Convert to string for session
            return redirect('add_marks_step2')
    else:
        form = SelectClassSubjectForm(teacher)

    return render(request, 'login/add_marks_step1.html', {'form': form})






@session_required('Teacher_login')
def add_marks_step2(request):
    username = request.session.get('login_username')
    teacher = get_object_or_404(TeacherAvailability, username=username)

    class_section_id = request.session.get('selected_class_section_id')
    subject_id = request.session.get('selected_subject_id')
    total_marks = request.session.get('total_marks')
    exam_type = request.session.get('exam_type')
    exam_date = request.session.get('exam_date')

    class_section = get_object_or_404(ClassSection, id=class_section_id)
    subject = get_object_or_404(Subject, id=subject_id)
    exam_date_obj = datetime.strptime(exam_date, "%Y-%m-%d").date()

    #level = ''.join(filter(str.isdigit, class_section.name))
    level = class_section.name


    students = Student.objects.filter(classlevel=level)
    student_data = [
        {'username': s.username, 'name': f"{s.student_first_name} {s.student_last_name}".strip()}
        for s in students
    ]

    if request.method == 'POST':
        form = EnterStudentMarksForm(student_data, request.POST)
        if form.is_valid():
            for student in student_data:
                uname = student['username']
                field_name = f'student_{uname}'
                mark = form.cleaned_data.get(field_name)

                try:
                    student_instance = Student.objects.get(username=uname)

                    if not Marks.objects.filter(
                        username=student_instance,
                        subject=subject,
                        added_by=teacher,
                        exam_type=exam_type,
                        exam_date=exam_date_obj
                    ).exists():
                        Marks.objects.create(
                            username=student_instance,
                            subject=subject,
                            marks=mark,
                            class_section=class_section,
                            exam_type=exam_type,
                            exam_date=exam_date_obj,
                            added_by=teacher
                        )
                except Student.DoesNotExist:
                    continue

            messages.success(request, "Marks added successfully.")
            return redirect('add_marks_step1')
    else:
        form = EnterStudentMarksForm(student_data)

    return render(request, 'login/add_marks_step2.html', {
        'form': form,
        'total_marks': total_marks,
        'class_section': class_section,
        'subject': subject,
        'exam_type': exam_type,
        'exam_date': exam_date
    })




@session_required('Student_login')
def view_marks(request):

    student_username = request.session.get('student_username')

    if not student_username:
        login_username = request.session.get('login_username')
        student_username = login_username
        request.session['student_username'] = student_username  

    try:
        student = Student.objects.get(username=student_username)
    except Student.DoesNotExist:
        messages.error(request, f"No student found with username '{student_username}' (possibly tampered).")
        return redirect('view_marks')  


    marks = Marks.objects.filter(username=student)
    available_subjects = Subject.objects.filter(id__in=marks.values_list('subject', flat=True).distinct())
    available_classes = ClassSection.objects.filter(id__in=marks.values_list('class_section', flat=True).distinct())
    selected_subject = request.GET.get('subject')
    selected_class = request.GET.get('class_section')
    sort_order = request.GET.get('sort')

    if selected_subject:
        marks = marks.filter(subject__id=selected_subject)

    if selected_class:
        marks = marks.filter(class_section__id=selected_class)

    if sort_order == 'asc':
        marks = marks.order_by('marks')
    elif sort_order == 'desc':
        marks = marks.order_by('-marks')

    return render(request, 'login/view_marks.html', {
        'student': student,
        'marks': marks,
        'available_subjects': available_subjects,
        'available_classes': available_classes,
        'selected_subject': selected_subject,
        'selected_class': selected_class,
        'sort_order': sort_order
    })





@csrf_exempt
@session_required('Student_login')
def set_sid_from_storage(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('student_username')
            if username:
                request.session['student_username'] = username
                return JsonResponse({'status': 'ok'})
        except json.JSONDecodeError:
            pass
    return JsonResponse({'status': 'invalid'}, status=400)
