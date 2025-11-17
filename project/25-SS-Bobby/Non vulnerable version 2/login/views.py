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



COUNTRIES = sorted([(country.name, country.name) for country in pycountry.countries])
BLOOD_GROUPS = [
    ('A+', 'A+'), ('A-', 'A-'),
    ('B+', 'B+'), ('B-', 'B-'),
    ('AB+', 'AB+'), ('AB-', 'AB-'),
    ('O+', 'O+'), ('O-', 'O-'),
]

# Add placeholder empty choices
NATIONALITY_CHOICES = [('', '--- Select Nationality ---')] + COUNTRIES
BLOOD_GROUP_CHOICES = [('', '--- Select Blood Group ---')] + BLOOD_GROUPS

class StudentApplicationForm(forms.Form):
    # Student Details
    student_first_name = forms.CharField(label="First Name", max_length=50)
    student_last_name = forms.CharField(label="Last Name", max_length=50)
    dob = forms.DateField(
        label="Date of Birth",
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    gender = forms.CharField(label="Gender", max_length=10, widget=forms.TextInput())

    student_email = forms.EmailField(label="Email")
    classlevel = forms.CharField(label="Class Level", max_length=10, widget=forms.TextInput())
    student_mobile = forms.CharField(label="Mobile Number", required=False)

    nationality = forms.ChoiceField(
        label="Nationality",
        choices=NATIONALITY_CHOICES,
        required=True
    )
    blood_group = forms.ChoiceField(
        label="Blood Group",
        choices=BLOOD_GROUP_CHOICES,
        required=True
    )

    # Student Address (now states optional)
    student_street = forms.CharField(label="Street", required=True)
    student_house = forms.CharField(label="House Number", required=True)
    student_city = forms.CharField(label="City/Town", required=True)
    student_state = forms.CharField(label="State/Province", required=False)  # Optional now
    student_postal = forms.CharField(label="Postal Code", required=True)

    # Parent/Guardian details
    parent_first_name = forms.CharField(label="Parent/Guardian First Name", required=True)
    parent_last_name = forms.CharField(label="Parent/Guardian Last Name", required=True)
    parent_email = forms.EmailField(label="Parent/Guardian Email", required=False)
    parent_mobile = forms.CharField(label="Parent/Guardian Mobile Number", required=False)
    emergency_contact = forms.CharField(label="Emergency Contact Number", required=False)

    # Parent/Guardian address (states optional here also)
    parent_street = forms.CharField(label="Street", required=True)
    parent_house = forms.CharField(label="House Number", required=True)
    parent_city = forms.CharField(label="City/Town", required=True)
    parent_state = forms.CharField(label="State/Province", required=False)  # Optional now
    parent_postal = forms.CharField(label="Postal Code", required=True)

    # Previous school details (optional)
    prev_school_name = forms.CharField(label="School Name", required=False)
    prev_class_grade = forms.FloatField(label="Previous Class Percentage", min_value=0.0, max_value=100.0, required=False)
    tc_number = forms.CharField(label="Transfer Certificate (TC) Number", required=False)

    # Previous school address (optional)
    prev_school_street = forms.CharField(label="Street", required=False)
    prev_school_house = forms.CharField(label="House Number", required=False)
    prev_school_city = forms.CharField(label="City/Town", required=False)
    prev_school_state = forms.CharField(label="State/Province", required=False)
    prev_school_postal = forms.CharField(label="Postal Code", required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Read-only fields
        readonly_fields = [
            'student_first_name', 'student_last_name',
            'dob', 'gender', 'student_email', 'classlevel'
        ]
        for field in readonly_fields:
            self.fields[field].widget.attrs['readonly'] = True
            self.fields[field].widget.attrs['style'] = 'background-color: #f0f0f0;'

        # Add red asterisk for required fields
        for name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(field.label + ' <span style="color:red">*</span>')

    # Custom validation for nationality and blood group
    def clean_nationality(self):
        value = self.cleaned_data.get('nationality')
        if not value or value == '':
            raise forms.ValidationError("Please select a nationality.")
        return value

    def clean_blood_group(self):
        value = self.cleaned_data.get('blood_group')
        if not value or value == '':
            raise forms.ValidationError("Please select a blood group.")
        return value
    
    
class StudentProfileForm(forms.Form):
    student_first_name = forms.CharField(max_length=100, required=True)
    student_last_name = forms.CharField(max_length=100, required=True)
    dob = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], required=True)
    student_email = forms.EmailField(required=True)

    classlevel = forms.CharField(max_length=8, required=False)

    student_mobile = forms.CharField(max_length=15, required=False)
    nationality = forms.CharField(max_length=50, required=False)
    blood_group = forms.CharField(max_length=5, required=False)

    student_street = forms.CharField(max_length=100, required=False)
    student_house = forms.CharField(max_length=50, required=False)
    student_city = forms.CharField(max_length=50, required=False)
    student_state = forms.CharField(max_length=50, required=False)
    student_postal = forms.CharField(max_length=10, required=False)

    parent_first_name = forms.CharField(max_length=100, required=False)
    parent_last_name = forms.CharField(max_length=100, required=False)
    parent_email = forms.EmailField(required=False)
    parent_mobile = forms.CharField(max_length=15, required=False)
    emergency_contact = forms.CharField(max_length=15, required=False)

    parent_street = forms.CharField(max_length=100, required=False)
    parent_house = forms.CharField(max_length=50, required=False)
    parent_city = forms.CharField(max_length=50, required=False)
    parent_state = forms.CharField(max_length=50, required=False)

    profile_photo = forms.ImageField(required=False)

    readonly_fields = [
        'student_first_name',
        'student_last_name',
        'dob',
        'gender',
        'student_email',
        'classlevel'
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.readonly_fields:
            if field in self.fields:
                self.fields[field].widget.attrs['readonly'] = 'readonly'
                self.fields[field].widget.attrs['style'] = 'background-color: #e9ecef;'

class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['firstname', 'lastname', 'dob', 'gender', 'email', 'profile_photo', 'document']
        widgets = {
            'firstname': forms.TextInput(attrs={'style': 'background-color:#e9ecef;'}),
            'lastname': forms.TextInput(attrs={'style': 'background-color:#e9ecef;'}),
            'dob': forms.DateInput(attrs={'type': 'date', 'readonly': 'readonly', 'style': 'background-color:#e9ecef;'}),
            'gender': forms.Select(attrs={'disabled': True, 'style': 'background-color:#e9ecef;'}),
            'email': forms.EmailInput(attrs={'readonly': 'readonly', 'style': 'background-color:#e9ecef;'}),
        }

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


@session_required('Admin_login')
def student_approval(request):
    approved_emails = set(
        email.strip().lower()
        for email in Login.objects.filter(role='Student').values_list('email', flat=True)
        if email
    )
    all_students = StudentApplication.objects.all()
    pending_students = [s for s in all_students if s.student_email and s.student_email.strip().lower() not in approved_emails]
    return render(request, 'login/student_approval.html', {'students': pending_students})

@session_required('Admin_login')
def approve_student(request, student_id):
    student = get_object_or_404(StudentApplication, id=student_id)

    if Login.objects.filter(email__iexact=student.student_email, role='Student').exists():
        messages.warning(request, "Student already approved.")
        return redirect('student_approval')

    username = generate_username()
    password = generate_password()

    Student.objects.create(
        username=username,
        student_first_name=student.student_first_name,
        student_last_name=student.student_last_name,
        dob=student.dob,
        gender=student.gender,
        student_email=student.student_email,
        classlevel=student.classlevel,
        student_mobile=student.student_mobile,
        nationality=student.nationality,
        blood_group=student.blood_group,

        student_street=student.student_street,
        student_house=student.student_house,
        student_city=student.student_city,
        student_state=student.student_state,
        student_postal=student.student_postal,

        parent_first_name=student.parent_first_name,
        parent_last_name=student.parent_last_name,
        parent_email=student.parent_email,
        parent_mobile=student.parent_mobile,
        emergency_contact=student.emergency_contact,

        parent_street=student.parent_street,
        parent_house=student.parent_house,
        parent_city=student.parent_city,
        parent_state=student.parent_state,
    )

    Login.objects.create(
        username=username,
        password=password,
        role='Student',
        email=student.student_email.strip()
    )

    messages.success(request, "Student approved.")
    return redirect('student_approval')

@session_required('Admin_login')
def reject_student(request, student_id):
    student = get_object_or_404(StudentApplication, id=student_id)
    student.delete()
    messages.info(request, "Student application rejected.")
    return redirect('student_approval')


@session_required('Admin_login')
def teacher_approval(request):
    approved_emails = set(
        email.strip().lower()
        for email in Login.objects.filter(role='Teacher').values_list('email', flat=True)
        if email
    )
    all_teachers = TeacherReg.objects.all()
    pending_teachers = [t for t in all_teachers if t.email and t.email.strip().lower() not in approved_emails]
    return render(request, 'login/teacher_approval.html', {'teachers': pending_teachers})


@session_required('Admin_login')
def approve_teacher(request, teacher_id):
    teacher = get_object_or_404(TeacherReg, id=teacher_id)

    if Login.objects.filter(email__iexact=teacher.email, role='Teacher').exists():
        messages.warning(request, "Teacher already approved.")
        return redirect('teacher_approval')

    username = generate_username()
    password = generate_password()

    # Create entry in Teacher table
    Teacher.objects.create(
        username=username,
        firstname=teacher.firstname,
        lastname=teacher.lastname,
        dob=teacher.dob,
        gender=teacher.gender,
        email=teacher.email,
        document=teacher.document
    )

    # Create login entry
    Login.objects.create(
        username=username,
        password=password,
        role='Teacher',
        email=teacher.email.strip()
    )

    messages.success(request, "Teacher approved.")
    return redirect('teacher_approval')


@session_required('Admin_login')
def reject_teacher(request, teacher_id):
    teacher = get_object_or_404(TeacherReg, id=teacher_id)
    teacher.delete()
    messages.info(request, "Teacher registration rejected.")
    return redirect('teacher_approval')



@session_required('Student_login')
def student_profile(request):
    username = request.session.get('login_username')

    try:
        login_obj = Login.objects.get(username=username)
        student_app = StudentApplication.objects.get(student_email=login_obj.email)
        student_model = Student.objects.get(username=username)
    except (Login.DoesNotExist, StudentApplication.DoesNotExist, Student.DoesNotExist):
        messages.error(request, "Student data not found.")
        return redirect('student')

    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            new_photo = cleaned_data.get('profile_photo')

            update_student_fields = {}
            update_app_fields = {}

            for field, value in cleaned_data.items():
                if field in form.readonly_fields or field == 'profile_photo':
                    continue

                if hasattr(student_model, field) and getattr(student_model, field) != value:
                    update_student_fields[field] = value

                if hasattr(student_app, field) and getattr(student_app, field) != value:
                    update_app_fields[field] = value

            # Save photo if uploaded
            if new_photo:
                student_model.profile_photo = new_photo

            # Only save student_model if there are actual changes
            fields_to_update = list(update_student_fields.keys())
            if new_photo:
                fields_to_update.append('profile_photo')

            if fields_to_update:
                for field, value in update_student_fields.items():
                    setattr(student_model, field, value)
                student_model.save(update_fields=fields_to_update)

            # Update StudentApplication if needed
            if update_app_fields:
                StudentApplication.objects.filter(pk=student_app.pk).update(**update_app_fields)

            messages.success(request, "Profile updated successfully.")
            return redirect('student_profile')
    else:
        # Initial data from StudentApplication
        initial_data = {
            field: getattr(student_app, field)
            for field in StudentProfileForm.base_fields
            if hasattr(student_app, field)
        }
        form = StudentProfileForm(initial=initial_data)

    return render(request, 'login/student_profile.html', {
        'form': form,
        'profile_photo': student_model.profile_photo,
    })

@csrf_exempt  # Intentionally disable CSRF protection for demo/exploit
@session_required('Teacher_login')
def teacher_profile(request):
    # IDOR vulnerability: attacker can supply ?username=KP0001
    target_username = request.GET.get('username') or request.session.get('login_username')

    try:
        login_obj = Login.objects.get(username=target_username)
        teacher_reg = TeacherReg.objects.get(email=login_obj.email)
        teacher_model = Teacher.objects.get(username=target_username)
    except (Login.DoesNotExist, TeacherReg.DoesNotExist, Teacher.DoesNotExist):
        messages.error(request, "Teacher data not found.")
        return redirect('teacher')

    if request.method == 'POST':
        form = TeacherProfileForm(request.POST, request.FILES)
        updated_fields = []

        if form.is_valid():
            # Update text fields if changed
            new_firstname = form.cleaned_data.get('firstname')
            new_lastname = form.cleaned_data.get('lastname')

            if new_firstname and new_firstname != teacher_reg.firstname:
                teacher_reg.firstname = new_firstname
                teacher_model.firstname = new_firstname
                updated_fields.append('firstname')

            if new_lastname and new_lastname != teacher_reg.lastname:
                teacher_reg.lastname = new_lastname
                teacher_model.lastname = new_lastname
                updated_fields.append('lastname')

            # Update document if uploaded
            new_document = request.FILES.get('document')
            if new_document:
                try:
                    if teacher_reg.document and os.path.isfile(teacher_reg.document.path):
                        os.remove(teacher_reg.document.path)
                except Exception as e:
                    print(f"Document delete error: {e}")
                teacher_reg.document = new_document
                teacher_model.document = new_document
                updated_fields.append('document')

            # Update profile photo if uploaded
            new_photo = request.FILES.get('profile_photo')
            if new_photo:
                try:
                    if teacher_model.profile_photo and os.path.isfile(teacher_model.profile_photo.path):
                        os.remove(teacher_model.profile_photo.path)
                except Exception as e:
                    print(f"Photo delete error: {e}")
                teacher_model.profile_photo = new_photo
                updated_photo = True
            else:
                updated_photo = False

            # Save only if fields changed
            if updated_fields:
                teacher_reg.save(update_fields=updated_fields)
            if updated_fields or updated_photo:
                save_fields = ['firstname', 'lastname', 'document']
                if updated_photo:
                    save_fields.append('profile_photo')
                teacher_model.save(update_fields=save_fields)

            # Feedback messages
            if updated_fields or updated_photo:
                messages.success(request, "Profile updated successfully.")
            else:
                messages.info(request, "No changes were made.")

            return redirect('teacher_profile')
        else:
            messages.error(request, "Form data invalid.")
            return redirect('teacher_profile')

    else:
        # GET request: populate form with current data
        initial_data = {
            'firstname': teacher_reg.firstname,
            'lastname': teacher_reg.lastname,
            'dob': teacher_reg.dob,
            'gender': teacher_reg.gender,
            'email': teacher_reg.email,
        }
        form = TeacherProfileForm(initial=initial_data)

    return render(request, 'login/teacher_profile.html', {
        'form': form,
        'document_url': teacher_reg.document.url if teacher_reg.document else None,
        'profile_photo': teacher_model.profile_photo.url if teacher_model.profile_photo else None,
    })


@csrf_exempt  # Intentionally left CSRF vulnerable for teaching
@session_required('Teacher_login')
def download_teacher_document(request):
    username = request.session.get('login_username')
    try:
        login_obj = Login.objects.get(username=username)
        teacher_reg = TeacherReg.objects.get(email=login_obj.email)

        if not teacher_reg.document:
            messages.error(request, "No document uploaded.")
            return redirect('teacher_profile')

        document_path = teacher_reg.document.path
        if not os.path.exists(document_path):
            messages.error(request, "Document file not found on server.")
            return redirect('teacher_profile')

        return FileResponse(
            open(document_path, 'rb'),
            as_attachment=True,
            filename=os.path.basename(document_path)
        )

    except Login.DoesNotExist:
        messages.error(request, "Invalid teacher session.")
        return redirect('teacher')
    except TeacherReg.DoesNotExist:
        messages.error(request, "Teacher record not found.")
        return redirect('teacher')
    except Exception as e:
        print(f"[Download error] {e}")
        raise Http404("Unable to download file.")
    

@session_required('Admin_login')
def admin_profile(request):
    username = request.session.get('login_username')
    try:
        admin_obj = Login.objects.get(username=username, role='Admin')
    except Login.DoesNotExist:
        messages.error(request, "Admin data not found.")
        return redirect('admin')

    return render(request, 'login/admin_profile.html', {'admin': admin_obj})









def student_application_view(request):
    prefill_data = {}
    latest_reg = StudentReg.objects.last()  # adjust if needed

    GENDER_DISPLAY = {'M': 'Male', 'F': 'Female', 'O': 'Others'}

    if latest_reg:
        prefill_data = {
            'student_first_name': latest_reg.firstname,
            'student_last_name': latest_reg.lastname,
            'dob': latest_reg.dob,
            'gender': GENDER_DISPLAY.get(latest_reg.gender, latest_reg.gender),
            'student_email': latest_reg.email,
            'classlevel': f'Class {latest_reg.classlevel}',
        }

    if request.method == "POST":
        form = StudentApplicationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            StudentApplication.objects.create(
                student_first_name=data['student_first_name'],
                student_last_name=data['student_last_name'],
                dob=data['dob'],
                gender=data['gender'],
                student_email=data['student_email'],
                classlevel=data['classlevel'],
                student_mobile=data['student_mobile'],
                nationality=data['nationality'],
                blood_group=data['blood_group'],

                student_street=data['student_street'],
                student_house=data['student_house'],
                student_city=data['student_city'],
                student_state=data.get('student_state', ''),
                student_postal=data['student_postal'],

                parent_first_name=data['parent_first_name'],
                parent_last_name=data['parent_last_name'],
                parent_email=data['parent_email'],
                parent_mobile=data['parent_mobile'],
                emergency_contact=data['emergency_contact'],

                parent_street=data['parent_street'],
                parent_house=data['parent_house'],
                parent_city=data['parent_city'],
                parent_state=data.get('parent_state', ''),
                parent_postal=data['parent_postal'],

                prev_school_name=data['prev_school_name'],
                prev_class_grade=data['prev_class_grade'],
                tc_number=data['tc_number'],

                prev_school_street=data['prev_school_street'],
                prev_school_house=data['prev_school_house'],
                prev_school_city=data['prev_school_city'],
                prev_school_state=data['prev_school_state'],
                prev_school_postal=data['prev_school_postal']
            )
            messages.success(request, "Student application submitted successfully!")
            return redirect('index')
    else:
        form = StudentApplicationForm(initial=prefill_data)

    return render(request, "login/studentapplication.html", {"form": form})















