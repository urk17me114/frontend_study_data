import random
import string
from django.db import models
from django.core.validators import FileExtensionValidator

# Create your models here.

class Login(models.Model):
    username = models.CharField(max_length=6, primary_key=True)
    password = models.CharField(max_length=18)
    role = models.CharField(max_length=10)  # 'Student', 'Teacher', 'Admin'
    email = models.EmailField(null=True, blank=True)  # Add this field
    security_question = models.CharField(max_length=100, null=True)
    security_answer = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

    


class Student(models.Model):
    username = models.CharField(max_length=6, primary_key=True)
    firstname = models.CharField(max_length=50, null=False)
    lastname = models.CharField(max_length=50, null=False)
    email = models.CharField(max_length=100, null=False, unique=True)

    def __str__(self):
        return self.username
    


class Marks(models.Model):
    username = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    marks = models.IntegerField()
    added_by = models.CharField(max_length=100)



class StudentReg(models.Model):
    firstname =models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    dob = models.DateField()
    
    GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
]
    # Class level choices (Class 1 to Class 10)
    Class_level = [(str(i), f'Class {i}') for i in range(1, 11)]
    
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    email = models.EmailField(max_length=100)
    classlevel = models.CharField(max_length=2, choices=Class_level)
    def __str__(self):
        return f'{self.firstname} {self.lastname} {self.email}'
    


class TeacherReg(models.Model):
    firstname =models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    dob = models.DateField()
    
    GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
]
    
    
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    email = models.EmailField(max_length=100)
    document = models.FileField(
        upload_to='teacher_documents/',null=True, blank=True,  # Files will be saved in 'teacher_documents/' folder
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'docx', 'txt', 'jpg', 'png'])]
    )
    def __str__(self):
        return f'{self.firstname} {self.lastname} {self.email}'
    

    



class StudentApplication(models.Model):
    # Student Details
    student_first_name = models.CharField(max_length=100)
    student_last_name = models.CharField(max_length=100)
    dob = models.DateField()
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=7, choices=GENDER_CHOICES)
    
    student_email = models.EmailField()
    
    Class_level = [(str(i), f'Class {i}') for i in range(1, 11)]
    classlevel = models.CharField(max_length=8, choices=Class_level)
    
    student_mobile = models.CharField(max_length=15)
    nationality = models.CharField(max_length=50)
    blood_group = models.CharField(max_length=5)

    # Student Address
    student_street = models.CharField(max_length=100,)
    student_house = models.CharField(max_length=50,)
    student_city = models.CharField(max_length=50,)
    student_state = models.CharField(max_length=50,)
    student_postal = models.CharField(max_length=10,)

    # Parent/Guardian Details
    parent_first_name = models.CharField(max_length=100,)
    parent_last_name = models.CharField(max_length=100,)
    parent_email = models.EmailField()
    parent_mobile = models.CharField(max_length=15)
    emergency_contact = models.CharField(max_length=15)

    # Parent/Guardian Address
    parent_street = models.CharField(max_length=100,)
    parent_house = models.CharField(max_length=50,)
    parent_city = models.CharField(max_length=50,)
    parent_state = models.CharField(max_length=50,)
    parent_postal = models.CharField(max_length=10,)

    # Previous School Details
    prev_school_name = models.CharField(max_length=100,blank=True, null=True)
    prev_class_grade = models.CharField(max_length=10,blank=True, null=True)
    tc_number = models.CharField(max_length=50,blank=True, null=True)

    # Previous School Address
    prev_school_street = models.CharField(max_length=100,blank=True, null=True)
    prev_school_house = models.CharField(max_length=50,blank=True, null=True)
    prev_school_city = models.CharField(max_length=50,blank=True, null=True)
    prev_school_state = models.CharField(max_length=50,blank=True, null=True)
    prev_school_postal = models.CharField(max_length=10,blank=True, null=True)


    def __str__(self):
        return f"{self.student_first_name} {self.student_last_name}"

