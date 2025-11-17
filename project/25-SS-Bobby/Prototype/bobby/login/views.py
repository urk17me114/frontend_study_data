from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django import forms
from .models import Login, Student, Marks, StudentReg, TeacherReg
from django.contrib.auth import logout as django_logout
#from captcha.fields import CaptchaField
from .models import StudentApplication
from django.views.decorators.cache import never_cache
from functools import wraps
from django.shortcuts import get_object_or_404
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from django.core.cache import cache  # built-in Django cache
from django.http import JsonResponse
from captcha.models import CaptchaStore
from django.core.cache import cache
from django.urls import reverse
import time
from django.http import JsonResponse

CAPTCHA_REUSE_LIMIT = 10
CAPTCHA_TIME_WINDOW = 20  # seconds
FLAG = "🎉 FLAG{captcha_reuse_detected}"





import random
import string
import secrets
import pycountry
from .models import StudentReg
from django.utils.safestring import mark_safe







from functools import wraps
import random
import string
import secrets
from django.views.decorators.cache import never_cache
from django.db import connection
from django.http import JsonResponse

# --------- Forms ----------

class NewLoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=6, min_length=6)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    #captcha = CaptchaField()

    
class FeedbackForm(forms.Form):
    username = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    #captcha = CaptchaField()

class NewLoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=6, min_length=6)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    #captcha = CaptchaField()

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

class StudentRegistration(forms.Form):
    firstname = forms.CharField(label="Firstname", max_length=50)
    lastname = forms.CharField(label="Lastname", max_length=50)
    dob = forms.DateField(label="Date of Birth", widget=forms.DateInput(attrs={'type': 'date'}))
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = forms.ChoiceField(label="Gender", choices=GENDER_CHOICES, widget=forms.Select)
    email = forms.EmailField(label="Email")
    Class_level = [(str(i), f'Class {i}') for i in range(1, 11)]
    classlevel = forms.ChoiceField(label="Class level", choices=Class_level, widget=forms.Select)
    #captcha = CaptchaField()
    

class TeacherRegistration(forms.Form):
    firstname = forms.CharField(label="Firstname", max_length=50)
    lastname = forms.CharField(label="Lastname", max_length=50)
    dob = forms.DateField(label="Date of Birth", widget=forms.DateInput(attrs={'type': 'date'}))
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = forms.ChoiceField(label="Gender", choices=GENDER_CHOICES, widget=forms.Select)
    email = forms.EmailField(label="Email")
    document = forms.FileField(label="Upload CV", required=True, widget=forms.ClearableFileInput())
    #captcha = CaptchaField()
    

class MarksForm(forms.Form):
    student_username = forms.CharField(max_length=6)
    subject = forms.CharField(max_length=100)
    marks = forms.IntegerField()



# Dropdown choices for StudentApplication Form

COUNTRIES = sorted([(country.name, country.name) for country in pycountry.countries])

BLOOD_GROUPS = [
    ('A+', 'A+'), ('A-', 'A-'),
    ('B+', 'B+'), ('B-', 'B-'),
    ('AB+', 'AB+'), ('AB-', 'AB-'),
    ('O+', 'O+'), ('O-', 'O-'),
]

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
        choices=COUNTRIES,
        required=True
    )
    blood_group = forms.ChoiceField(
        label="Blood Group",
        choices=BLOOD_GROUPS,
        required=True
    )

    # Student Address (all required)
    student_street = forms.CharField(label="Street", required=True)
    student_house = forms.CharField(label="House Number", required=True)
    student_city = forms.CharField(label="City/Town", required=True)
    student_state = forms.CharField(label="State/Province", required=True)
    student_postal = forms.CharField(label="Postal Code", required=True)

    # Parent/Guardian details
    parent_first_name = forms.CharField(label="Parent/Guardian First Name", required=True)
    parent_last_name = forms.CharField(label="Parent/Guardian Last Name", required=True)
    parent_email = forms.EmailField(label="Parent/Guardian Email", required=False)
    parent_mobile = forms.CharField(label="Parent/Guardian Mobile Number", required=False)
    emergency_contact = forms.CharField(label="Emergency Contact Number", required=False)

    # Parent/Guardian address (all required)
    parent_street = forms.CharField(label="Street", required=True)
    parent_house = forms.CharField(label="House Number", required=True)
    parent_city = forms.CharField(label="City/Town", required=True)
    parent_state = forms.CharField(label="State/Province", required=True)
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




# --------- Helper Function ----------
class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label="Old Password", widget=forms.PasswordInput)
    new_password = forms.CharField(label="New Password", widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Confirm New Password", widget=forms.PasswordInput)

class ForgotPasswordForm(forms.Form):
    username = forms.CharField(label="Username", max_length=6, min_length=6)

class SecurityAnswerForm(forms.Form):
    answer = forms.CharField(label="Your Answer", widget=forms.TextInput())

class ResetPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

class SecurityQuestionForm(forms.Form):
    SECURITY_QUESTIONS = [
    ('What is your mother’s maiden name?', 'What is your mother’s maiden name?'),
    ('What was the name of your first pet?', 'What was the name of your first pet?'),
    ('What is your favorite book?', 'What is your favorite book?'),
    ('What city were you born in?', 'What city were you born in?'),
    ('What is your favorite teacher’s name?', 'What is your favorite teacher’s name?'),]

    security_question = forms.ChoiceField(label="Security Question", choices=SECURITY_QUESTIONS)
    security_answer = forms.CharField(label="Answer", max_length=100)

class SearchForm(forms.Form):
    query = forms.CharField(label="Search Username", max_length=100, required=True)


# --------- Helper Functions ----------
def generate_username():
    letters = ''.join(random.choices(string.ascii_uppercase, k=3))
    digits = ''.join(random.choices(string.digits, k=3))
    return letters + digits

def generate_password():
    return secrets.token_urlsafe(8)

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

def search_student(request):
    results = None
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            
            # WARNING: Vulnerable to SQL Injection by directly formatting user input into SQL
            raw_sql = f"SELECT * FROM login_student WHERE firstname LIKE '%{query}%'"
            
            with connection.cursor() as cursor:
                cursor.execute(raw_sql)
                columns = [col[0] for col in cursor.description]
                results = [
                    dict(zip(columns, row))
                    for row in cursor.fetchall()
                ]
    else:
        form = SearchForm()
    
    return render(request, "login/search.html", {"form": form, "results": results})
@never_cache
@session_required('Admin_login')
def admin_dashboard(request):


    functionalities = [
        {'label': 'Register Users', 'url_name': 'registration'},
        {'label': 'Change Password', 'url_name': 'change_password'},
        {'label': 'Search Student', 'url_name': 'search_student'},
    ]

    return render(request, 'login/dashboard.html', {'role': 'Admin', 'functionalities': functionalities})

@never_cache
@session_required('Teacher_login')
def teacher_dashboard(request):


    functionalities = [
        {'label': 'Add Marks', 'url_name': 'add_marks'},
        {'label': 'Change Password', 'url_name': 'change_password'},
    ]

    return render(request, 'login/dashboard.html', {'role': 'Teacher', 'functionalities': functionalities})


@never_cache
@session_required('Student_login')
def student_dashboard(request):


    functionalities = [
        {'label': 'View Marks', 'url_name': 'view_marks'},
        {'label': 'Change Password', 'url_name': 'change_password'},
    ]
    context = {
        'role': 'Student',
        'functionalities': functionalities
    }
    return render(request, 'login/dashboard.html', {'role': 'Student', 'functionalities': functionalities})


from captcha.models import CaptchaStore

def validate_captcha_manual(captcha_id, captcha_response):
    try:
        captcha = CaptchaStore.objects.get(hashkey=captcha_id)
        return captcha.response == captcha_response.lower()  # lowercase to match
    except CaptchaStore.DoesNotExist:
        return False


def index(request):
    if request.method == "POST":
        form = NewLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username'].strip()
            password = form.cleaned_data['password'].strip()
            try:
                login = Login.objects.get(username=username)
                if login.password == password:
                    request.session.flush()
                    request.session[f'{login.role}_login'] = True
                    request.session['login_username'] = username
                    request.session['current_role'] = login.role
                    if login.role == 'Admin':
                        return redirect('admin')
                    elif login.role == 'Teacher':
                        return redirect('teacher')
                    elif login.role == 'Student':
                        return redirect('student')
                else:
                    form.add_error(None, 'Incorrect password')
            except Login.DoesNotExist:
                form.add_error(None, 'Invalid credentials')
    else:
        form = NewLoginForm()
    return render(request, "login/login.html", {"form": form})


def logout_view(request):
    request.session.flush()
    return redirect('index')



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
    students = StudentApplication.objects.all()
    return render(request, 'login/student_approval.html', {'students': students})

@session_required('Admin_login')
def approve_student(request, student_id):
    student = get_object_or_404(StudentApplication, id=student_id)
    username = generate_username()
    password = generate_password()

    Student.objects.create(
        username=username,
        firstname=student.student_first_name,
        lastname=student.student_last_name,
        email=student.student_email
    )

    Login.objects.create(
        username=username,
        password=password,
        role='Student',
        email=student.student_email
    )

    messages.success(request, f"Student approved.")
    student.delete()
    return redirect('student_approval')

@session_required('Admin_login')
def reject_student(request, student_id):
    student = get_object_or_404(StudentApplication, id=student_id)
    student.delete()
    messages.info(request, "Student application rejected.")
    return redirect('student_approval')


@session_required('Admin_login')
def teacher_approval(request):
    teachers = TeacherReg.objects.all()
    return render(request, 'login/teacher_approval.html', {'teachers': teachers})

@session_required('Admin_login')
def approve_teacher(request, teacher_id):
    teacher = get_object_or_404(TeacherReg, id=teacher_id)
    username = generate_username()
    password = generate_password()

    Login.objects.create(
        username=username,
        password=password,
        role='Teacher',
        email=teacher.email
    )

    messages.success(request, f"Teacher approved.")
    teacher.delete()
    return redirect('teacher_approval')

@session_required('Admin_login')
def reject_teacher(request, teacher_id):
    teacher = get_object_or_404(TeacherReg, id=teacher_id)
    teacher.delete()
    messages.info(request, "Teacher registration rejected.")
    return redirect('teacher_approval')


@session_required('Teacher_login')
def add_marks(request):
    if request.method == 'POST':
        form = MarksForm(request.POST)
        if form.is_valid():
            student_username = form.cleaned_data['student_username']
            subject = form.cleaned_data['subject']
            marks = form.cleaned_data['marks']
            try:
                student = Student.objects.get(username=student_username)
                Marks.objects.create(
                    username=student,
                    subject=subject,
                    marks=marks,
                    added_by=request.session['login_username']
                )
                messages.success(request, "Marks added successfully.")
                return redirect('add_marks')
            except Student.DoesNotExist:
                form.add_error('student_username', 'Student not found.')
    else:
        form = MarksForm()
    return render(request, 'login/add_marks.html', {'form': form})

@session_required('Student_login')
def view_marks(request):
    username = request.session.get('login_username')
    try:
        student = Student.objects.get(username=username)
        marks = Marks.objects.filter(username=student)
        return render(request, 'login/greet.html', {'student': student, 'marks': marks})
    except Student.DoesNotExist:
        return HttpResponse("Student not found.")

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
                if user.password != old_password:
                    form.add_error('old_password', 'Old password is incorrect.')
                elif new_password != confirm_password:
                    form.add_error('confirm_password', 'New passwords do not match.')
                else:
                    user.password = new_password
                    user.save()
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


@never_cache
def forgot_password_step1(request):
    request.session.pop('forgot_username', None)
    request.session.pop('forgot_verified', None)

    if request.method == "POST":
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            try:
                user = Login.objects.get(username=username)
                # Save username in session for next steps
                request.session['forgot_username'] = username
                return redirect('forgot_password_step2')
            except Login.DoesNotExist:
                form.add_error('username', 'Username not found.')
    else:
        form = ForgotPasswordForm()

    return render(request, "login/forgot_password.html", {"form": form})

@never_cache
@session_required('forgot_username')
def forgot_password_step2(request):
    username = request.session.get('forgot_username')


    try:
        user = Login.objects.get(username=username)
    except Login.DoesNotExist:
        messages.error(request, "User not found.")
        request.session.flush()
        return redirect('forgot_password_step1')

    if not user.security_question:
        messages.warning(request, "No security question. Please contact admin.")
        return redirect('index')

    if request.method == "POST":
        form = SecurityAnswerForm(request.POST)
        if form.is_valid():
            answer = form.cleaned_data['answer']
            if answer.strip().lower() == user.security_answer.strip().lower():
                # Mark that security answer is verified
                request.session['forgot_verified'] = True
                return redirect('forgot_password_step3')
            else:
                form.add_error('answer', 'Incorrect answer.')
    else:
        form = SecurityAnswerForm()

    return render(request, "login/security_question.html", {
        "form": form,
        "question": user.security_question
    })

@never_cache
@session_required('forgot_username')

def forgot_password_step3(request):
    username = request.session.get('forgot_username')
    verified = request.session.get('forgot_verified')



    try:
        user = Login.objects.get(username=username)
    except Login.DoesNotExist:
        messages.error(request, "User not found.")
        request.session.flush()
        return redirect('forgot_password_step1')

    if user.security_question and not verified:
        messages.error(request, "Access denied. You must answer your security question first.")
        return redirect('forgot_password_step1')

    if request.method == "POST":
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            confirm = form.cleaned_data['confirm_password']
            if password != confirm:
                form.add_error('confirm_password', "Passwords do not match.")
            else:
                user.password = password
                user.save()
                messages.success(request, "Password reset successful.")
                # Clear all related session keys
                request.session.pop('forgot_username', None)
                request.session.pop('forgot_verified', None)
                return redirect('index')
    else:
        form = ResetPasswordForm()

    return render(request, "login/reset_password.html", {"form": form})


def student_registration(request):
    if request.method == "POST":

        captcha_id = request.POST.get('captcha_0')
        captcha_response = request.POST.get('captcha_1')

        # Manual CAPTCHA check (VULNERABLE: allows reuse)
        if not validate_captcha_manual(captcha_id, captcha_response):
            messages.error(request, "Invalid CAPTCHA.")
            return redirect('studentregistration')
        

        reuse_key = f"captcha_reuse_{captcha_id}"
        reuse_data = cache.get(reuse_key, [])
        current_time = time.time()

        # Only keep timestamps within last 20 seconds
        reuse_data = [t for t in reuse_data if current_time - t <= CAPTCHA_TIME_WINDOW]
        reuse_data.append(current_time)
        cache.set(reuse_key, reuse_data, timeout=60)

        if len(reuse_data) >= CAPTCHA_REUSE_LIMIT:
            return JsonResponse({
                "status": "success",
                "message": "CAPTCHA replay successful! Vulnerability confirmed.",
                "flag": FLAG
            })
        
        
        form = StudentRegistration(request.POST)
        if form.is_valid():
            firstname = form.cleaned_data['firstname']
            lastname = form.cleaned_data['lastname']
            dob = form.cleaned_data['dob']
            gender = form.cleaned_data['gender']
            email = form.cleaned_data['email']
            classlevel = form.cleaned_data['classlevel']

            StudentReg.objects.create(
                firstname=firstname,
                lastname=lastname,
                dob=dob,
                gender=gender,
                email=email,
                classlevel=classlevel
            )
            messages.success(request, "Student registered successfully!")
            return redirect('studentapplication')  # Redirect to same page or success page
            
    else:
        form = StudentRegistration()
        new_captcha = CaptchaStore.generate_key()
        captcha_image = captcha_image_url(new_captcha)


    return render(request, "login/studentregistration.html", {
        "form": form,
        "captcha_key": new_captcha,
        "captcha_image_url": captcha_image
    })

def teacher_registration(request):
    if request.method == "POST":
        form = TeacherRegistration(request.POST, request.FILES)
        if form.is_valid():
            firstname = form.cleaned_data['firstname']
            lastname = form.cleaned_data['lastname']
            dob = form.cleaned_data['dob']
            gender = form.cleaned_data['gender']
            email = form.cleaned_data['email']
            document = form.cleaned_data['document']

            teacher = TeacherReg.objects.create(
                firstname=firstname,
                lastname=lastname,
                dob=dob,
                gender=gender,
                email=email
            )

            if document:
                # **Vulnerable File Type Check**
                allowed_extensions = ['.jpg', '.png', '.pdf', '.doc', '.docx', '.jpeg']
                max_file_size = 7 * 1024 * 1024  # 7 MB in bytes

                if not any(document.name.endswith(ext) for ext in allowed_extensions):
                    messages.error(request, "Invalid file type. Only .jpg, .png, .pdf, .doc, .docx, .jpeg files are allowed.")
                    return redirect('teacherregistration')
                
                    
                
                if document.size > max_file_size:
                    messages.error(request, "File size exceeds the maximum limit of 7 MB.")
                    return redirect('teacherregistration')
                
                else:
                    teacher.document = document
                    teacher.save()

            messages.success(request, "Teacher registered successfully!")
            return redirect('index')
    else:
        form = TeacherRegistration()
    return render(request, "login/teacherregistration.html", {"form": form})



def student_application_view(request):
    prefill_data = {}
    latest_reg = StudentReg.objects.last()  # You can improve this later using session/email

    # Mapping codes to display labels
    GENDER_DISPLAY = {'M': 'Male', 'F': 'Female', 'O': 'Others'}

    if latest_reg:
        prefill_data = {
            'student_first_name': latest_reg.firstname,
            'student_last_name': latest_reg.lastname,
            'dob': latest_reg.dob,
            'gender': GENDER_DISPLAY.get(latest_reg.gender, latest_reg.gender),  # Convert 'M' to 'Male'
            'student_email': latest_reg.email,
            'classlevel': f'Class {latest_reg.classlevel}',  # Convert '1' to 'Class 1'
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
                student_state=data['student_state'],
                student_postal=data['student_postal'],

                parent_first_name=data['parent_first_name'],
                parent_last_name=data['parent_last_name'],
                parent_email=data['parent_email'],
                parent_mobile=data['parent_mobile'],
                emergency_contact=data['emergency_contact'],

                parent_street=data['parent_street'],
                parent_house=data['parent_house'],
                parent_city=data['parent_city'],
                parent_state=data['parent_state'],
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

