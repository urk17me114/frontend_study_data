import random
import string
from django.db import models
from django.core.validators import FileExtensionValidator

# Create your models here.
class Login(models.Model):
    username = models.CharField(max_length=6, primary_key=True)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=10, null=False)  # 'Student', 'Teacher', 'Admin'
    email = models.EmailField(null=True, blank=True)  # Add this field
    security_question = models.CharField(max_length=100, null=True)
    security_answer = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"
    

class Login2(models.Model):
    username = models.CharField(max_length=6, primary_key=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.username} ({self.role})"


class Student(models.Model):
    username = models.CharField(max_length=6, primary_key=True)

    # Student Info
    student_first_name = models.CharField(max_length=100, null=True, blank=True)
    student_last_name = models.CharField(max_length=100, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=7, null=True, blank=True)
    student_email = models.EmailField(null=True, blank=True)
    classlevel = models.CharField(max_length=8, null=True, blank=True)
    student_mobile = models.CharField(max_length=15, null=True, blank=True)
    nationality = models.CharField(max_length=50, null=True, blank=True)
    blood_group = models.CharField(max_length=5, null=True, blank=True)

    # Student Address
    student_street = models.CharField(max_length=100, null=True, blank=True)
    student_house = models.CharField(max_length=50, null=True, blank=True)
    student_city = models.CharField(max_length=50, null=True, blank=True)
    student_state = models.CharField(max_length=50, null=True, blank=True)
    student_postal = models.CharField(max_length=10, null=True, blank=True)

    # Parent/Guardian Info
    parent_first_name = models.CharField(max_length=100, null=True, blank=True)
    parent_last_name = models.CharField(max_length=100, null=True, blank=True)
    parent_email = models.EmailField(null=True, blank=True)
    parent_mobile = models.CharField(max_length=15, null=True, blank=True)
    emergency_contact = models.CharField(max_length=15, null=True, blank=True)

    # Parent Address
    parent_street = models.CharField(max_length=100, null=True, blank=True)
    parent_house = models.CharField(max_length=50, null=True, blank=True)
    parent_city = models.CharField(max_length=50, null=True, blank=True)
    parent_state = models.CharField(max_length=50, null=True, blank=True)

    profile_photo = models.ImageField(upload_to='student_photos/', null=True, blank=True)

    def __str__(self):
        return self.username
    
class Teacher(models.Model):
    username = models.CharField(max_length=6, primary_key=True)
    firstname = models.CharField(max_length=100, null=True, blank=True)
    lastname = models.CharField(max_length=100, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    #subjects = models.ManyToManyField('Subject')
    #max_periods_per_day = models.IntegerField(default=6)
    #max_periods_per_week = models.IntegerField(default=30)
    #unavailable = models.ManyToManyField('TimeSlot', blank=True)

    document = models.FileField(
        upload_to='teacher_documents/',
        null=True,
        blank=True,
        #validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    )

    profile_photo = models.ImageField(upload_to='teacher_photos/', null=True, blank=True)

    def __str__(self):
        return self.username

class Teachers(models.Model):
    username = models.CharField(max_length=6, primary_key=True)
    firstname = models.CharField(max_length=50, null=False)
    lastname = models.CharField(max_length=50, null=False)
    email = models.CharField(max_length=100, null=False, unique=True)

    role = models.CharField(
        max_length=10,
        editable=False,
        default='teacher'
    )

    def __str__(self):
        return f"{self.firstname} {self.lastname} ({self.username})"


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
    
class StudentReg1(models.Model):
    username = models.CharField(max_length=6, primary_key=True)
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
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    dob = models.DateField()
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    email = models.EmailField(max_length=100)
    document = models.FileField(upload_to='teacher_documents/', null=True, blank=True,)
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

    # Student Address (student_state optional)
    student_street = models.CharField(max_length=100)
    student_house = models.CharField(max_length=50)
    student_city = models.CharField(max_length=50)
    student_state = models.CharField(max_length=50, blank=True, null=True)  # optional
    student_postal = models.CharField(max_length=10)

    # Parent/Guardian Details
    parent_first_name = models.CharField(max_length=100)
    parent_last_name = models.CharField(max_length=100)
    parent_email = models.EmailField()
    parent_mobile = models.CharField(max_length=15)
    emergency_contact = models.CharField(max_length=15)

    # Parent/Guardian Address (parent_state optional)
    parent_street = models.CharField(max_length=100)
    parent_house = models.CharField(max_length=50)
    parent_city = models.CharField(max_length=50)
    parent_state = models.CharField(max_length=50, blank=True, null=True)  # optional
    parent_postal = models.CharField(max_length=10)

    # Previous School Details (optional)
    prev_school_name = models.CharField(max_length=100, blank=True, null=True)
    prev_class_grade = models.CharField(max_length=10, blank=True, null=True)
    tc_number = models.CharField(max_length=50, blank=True, null=True)

    # Previous School Address (optional)
    prev_school_street = models.CharField(max_length=100, blank=True, null=True)
    prev_school_house = models.CharField(max_length=50, blank=True, null=True)
    prev_school_city = models.CharField(max_length=50, blank=True, null=True)
    prev_school_state = models.CharField(max_length=50, blank=True, null=True)
    prev_school_postal = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.student_first_name} {self.student_last_name}"
    







DAYS = [('Mon','Mon'), ('Tue','Tue'), ('Wed','Wed'), ('Thu','Thu'), ('Fri','Fri')]

class Subject(models.Model):
    name = models.CharField(max_length=50)
    periods_per_week = models.IntegerField()
    specialized_room = models.CharField(max_length=50, blank=True)
    def __str__(self): return self.name


    
class ClassSection(models.Model):
    name = models.CharField(max_length=20)
    subjects = models.ManyToManyField(Subject)
    def __str__(self): return self.name



class TimeSlot(models.Model):
    day = models.CharField(max_length=3, choices=DAYS)
    period = models.IntegerField()
    def __str__(self): return f"{self.day} P{self.period}"

class TeacherAvailability(models.Model):
    username = models.CharField(max_length=6, unique=True)
    name = models.CharField(max_length=100)
    subjects = models.ManyToManyField(Subject)
    class_sections = models.ManyToManyField(ClassSection)
    max_periods_per_day = models.IntegerField(default=6)
    max_periods_per_week = models.IntegerField(default=30)
    unavailable = models.ManyToManyField(TimeSlot, blank=True)

    def __str__(self):
        return self.name


class Room(models.Model):
    name = models.CharField(max_length=50)  # renamed from 'room' to 'name'
    room_type = models.CharField(max_length=50, default='Regular')

    def __str__(self):
        return f"{self.name} ({self.room_type})"
    
class TimetableEntry(models.Model):
    class_section = models.ForeignKey(ClassSection, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(TeacherAvailability, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.class_section} · {self.timeslot}: {self.subject} [{self.teacher}]"
    

EXAM_TYPE_CHOICES = [
    ('Midterm', 'Midterm'),
    ('Final', 'Final'),
    ('Quiz', 'Quiz'),
    ('Assignment', 'Assignment'),
]

class Marks(models.Model):
    username = models.ForeignKey(Student, to_field='username', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    class_section = models.ForeignKey(ClassSection, on_delete=models.CASCADE)
    marks = models.IntegerField()
    exam_type = models.CharField(max_length=50, choices=EXAM_TYPE_CHOICES)
    exam_date = models.DateField()
    added_by = models.ForeignKey(TeacherAvailability, to_field='username', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('username', 'subject', 'added_by', 'class_section', 'exam_type', 'exam_date')

    def __str__(self):
        return f"{self.username} - {self.subject} - {self.exam_type} ({self.exam_date}) - {self.marks}"

class Question(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    text = models.TextField()

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    text = models.TextField()
    like_count = models.PositiveIntegerField(default=0)

class TeacherAnnouncement(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    text = models.TextField()
    pdf_file = models.FileField(upload_to='announcements_pdfs/', blank=True, null=True)  # Optional PDF
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Announcement by {self.teacher.username} on {self.created_at}"
    
class AnnouncementVote(models.Model):
    announcement = models.ForeignKey(TeacherAnnouncement, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=10, choices=[('upvote', 'Upvote'), ('downvote', 'Downvote')])

    class Meta:
        unique_together = ('announcement', 'student') # Each student can vote only once per announcement

    