from django import forms
from .models import Subject, TeacherAvailability, ClassSection, Room, TimeSlot, Teacher

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(SubjectForm, self).__init__(*args, **kwargs)
        room_types = Room.objects.values_list('room_type', flat=True).distinct()
        choices = [(r, r) for r in sorted(room_types) if r]
        self.fields['specialized_room'] = forms.ChoiceField(choices=choices, required=False)

class TeacherForm(forms.ModelForm):
    teacher = forms.ModelChoiceField(
        queryset=Teacher.objects.all(),
        label='Select Teacher',
        widget=forms.Select(attrs={'onchange': 'fillUsername(this)'})
    )

    class Meta:
        model = TeacherAvailability
        fields = ['username', 'name', 'teacher', 'subjects', 'class_sections', 'max_periods_per_day', 'max_periods_per_week', 'unavailable']
        widgets = {
            'username': forms.TextInput(attrs={'readonly': 'readonly'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(TeacherForm, self).__init__(*args, **kwargs)
        self.fields['teacher'].label_from_instance = lambda obj: f"{obj.firstname} {obj.lastname}"

class ClassSectionForm(forms.ModelForm):
    class Meta:
        model = ClassSection
        fields = '__all__'

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'

class TimeSlotForm(forms.ModelForm):
    class Meta:
        model = TimeSlot
        fields = '__all__'

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label="Old Password", widget=forms.PasswordInput)
    new_password = forms.CharField(label="New Password", widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Confirm New Password", widget=forms.PasswordInput)

class ForgotPasswordForm(forms.Form):
    username = forms.CharField(label="Username", max_length=6, min_length=6)

class SecurityAnswerForm(forms.Form):
    question = forms.CharField(label="Security Question", widget=forms.TextInput(attrs={'readonly': 'readonly'}))
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

class SearchFormStudent(forms.Form):
    query = forms.CharField(label="Search Student", max_length=200, required=True)

class SearchFormTeacher(forms.Form):
    query = forms.CharField(label="Search Teacher", max_length=200, required=True)

EXAM_TYPE_CHOICES = [
    ('Midterm', 'Midterm'),
    ('Final', 'Final'),
    ('Quiz', 'Quiz'),
    ('Assignment', 'Assignment'),
]
 
class SelectClassSubjectForm(forms.Form):
    class_section = forms.ModelChoiceField(queryset=ClassSection.objects.none(), label="Class")
    subject = forms.ModelChoiceField(queryset=Subject.objects.none())
    total_marks = forms.IntegerField(min_value=0)
    exam_type = forms.ChoiceField(choices=EXAM_TYPE_CHOICES)
    exam_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    def __init__(self, teacher, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['class_section'].queryset = teacher.class_sections.all()
        self.fields['subject'].queryset = teacher.subjects.all()


class EnterStudentMarksForm(forms.Form):
    def __init__(self, student_data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for student in student_data:
            uname = student['username']
            full_name = student['name']
            field_name = f'student_{uname}'
            self.fields[field_name] = forms.IntegerField(
                label=f"{full_name} ({uname})",
                min_value=0,
                required=True
            )


class NewLoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


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

class QuestionForm(forms.Form):
    
        question_text = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}))



class TeacherAnnouncementForm(forms.Form):
    announcement_text = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), label = "Announcement")
    pdf_file = forms.FileField(
        required=False,
        label="Attach file",
        widget=forms.ClearableFileInput(attrs={'accept': '.pdf'})
    )