from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.hashers import check_password
from . import templates
from .models import Student, teacher
from .models import UserAccount
from django.utils.crypto import get_random_string
from .forms import StudentForm

# Create your views here.
def index(request):
    return HttpResponse("Hello student")


def index9(request):
    return HttpResponse("Hello Teacher")

def index2(request):
    return HttpResponse("login credentials created successfully")

def index3(request):
    return render(request, "login/greet.html")
def index4(request):
    if request.method == "POST":
        # Save the form data into the database
        Student.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            dob=request.POST['dob'],
            gender=request.POST['gender'],
            email=request.POST['email'],
            class_applied=request.POST['class_applied']
        )
        return redirect('index3')  # Redirect to the greet page
    return render(request, "login/studentregister.html")





def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = UserAccount.objects.get(username=username)

            if password == user.password:
                # Redirect to different pages based on role
                if user.role == 'admin':
                    return render(request, 'login/adminwelcomepage.html')
                elif user.role == 'student':
                    return render(request, 'login/studentwelcomepage.html')  # replace with actual path
                elif user.role == 'teacher':
                    return render(request, 'login/teacherwelcomepage.html')  # replace with actual path
                else:
                    return render(request, 'login/greet.html', {'error': 'Unknown role'})
            else:
                return render(request, 'login/greet.html', {'error': 'Invalid password'})
        
        except UserAccount.DoesNotExist:
            return render(request, 'login/greet.html', {'error': 'Invalid username'})

    return render(request, 'login/greet.html')



def index5(request):
    return render(request, "login/adminwelcomepage.html")



def index6(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        dob = request.POST['dob']

        try:
            # Check if student exists
            student = Student.objects.get(first_name=first_name, last_name=last_name, dob=dob)

            # Generate username and password
            username = f"{first_name.lower()}{last_name.lower()}{get_random_string(3)}"
            password = get_random_string(8)
            role = 'student'

            # Save credentials to UserAccount table
            UserAccount.objects.create(
                username=username,
                password=password,
                role=role
            )

            # Redirect or show success
            return redirect('index2')  # or any page you prefer (e.g., a success page)

        except Student.DoesNotExist:
            return render(request, 'login/createstudentcredentials.html', {
                'error': 'Student not found.'
            })

    return render(request, 'login/createstudentcredentials.html')


def index7(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        dob = request.POST['dob']

        try:
            # Check if student exists
            student = teacher.objects.get(first_name=first_name, last_name=last_name, dob=dob)

            # Generate username and password
            username = f"{first_name.lower()}{last_name.lower()}{get_random_string(3)}"
            password = get_random_string(8)
            role = 'teacher'

            # Save credentials to UserAccount table
            UserAccount.objects.create(
                username=username,
                password=password,
                role=role
            )

            # Redirect or show success
            return redirect('index2')  # or any page you prefer (e.g., a success page)

        except teacher.DoesNotExist:
            return render(request, 'login/createteachercredentials.html', {
                'error': 'Teacher not found.'
            })

    return render(request, 'login/createteachercredentials.html')

def index8(request):
    if request.method == "POST":
        # Save the form data into the database
        teacher.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            dob=request.POST['dob'],
            gender=request.POST['gender'],
            email=request.POST['email']
            
        )
        return redirect('index3')  # Redirect to the greet page
    return render(request, "login/teacherregister.html")


def index9(request):
    return render(request, "login/studentwelcomepage.html")


def index10(request):
    return render(request, "login/teacherwelcomepage.html")


def student_list(request):
    students = Student.objects.all()
    return render(request, 'student_list.html', {'students': students})

def edit_student(request, student_id):
    student = get_object_or_404(Student, pk=student_id)

    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)

    return render(request, 'edit_student.html', {'form': form, 'student': student})












