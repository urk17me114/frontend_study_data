from django import forms
from .models import Subject, TeacherAvailability, ClassSection, Room, TimeSlot, Teacher, StudentAssignment, AssignmentQuestion, AssignmentSubmission
from .models import Login, Student, Marks, StudentReg, TeacherReg, TimetableEntry,  TeacherAvailability, StudentReg1, Teachers, Answer, Question, Login2
from .models import StudentApplication
from .models import Pinboard, PinboardComment
import pycountry
from django.utils.safestring import mark_safe


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

from django import forms
from .models import StudentAssignment, Subject, ClassSection

class StudentAssignmentForm(forms.ModelForm):
    class Meta:
        model = StudentAssignment
        fields = ["title", "description", "subject", "file"]

class AssignmentFilterForm(forms.Form):
    subject = forms.ModelChoiceField(queryset=Subject.objects.none(), required=False)
    class_section = forms.ModelChoiceField(queryset=ClassSection.objects.none(), required=False)

    def __init__(self, *args, teacher=None, **kwargs):
        super().__init__(*args, **kwargs)
        if teacher:
            self.fields['subject'].queryset = Subject.objects.filter(teacheravailability__username=teacher.username)
            self.fields['class_section'].queryset = ClassSection.objects.filter(teacheravailability__username=teacher.username)


class AssignmentQuestionForm(forms.ModelForm):
    class Meta:
        model = AssignmentQuestion
        fields = ['title', 'description', 'subject', 'class_section', 'attachment', 'due_date']

class AssignmentSubmissionForm(forms.ModelForm):
    class Meta:
        model = AssignmentSubmission
        fields = ['file', 'comment']

class GradeSubmissionForm(forms.ModelForm):
    class Meta:
        model = AssignmentSubmission
        fields = ['marks', 'feedback']
        widgets = {
            'feedback': forms.Textarea(attrs={'rows': 4})
        }

class SubmissionFilterForm(forms.Form):
    subject = forms.ModelChoiceField(queryset=None, required=False)
    class_section = forms.ModelChoiceField(queryset=None, required=False)
    status = forms.ChoiceField(choices=[('', '---')] + AssignmentSubmission.STATUS_CHOICES, required=False)

    def __init__(self, *args, teacher=None, **kwargs):
        super().__init__(*args, **kwargs)
        if teacher:
            self.fields['subject'].queryset = teacher.subjects.all()
            self.fields['class_section'].queryset = teacher.class_sections.all()
        else:
            self.fields['subject'].queryset = []
            self.fields['class_section'].queryset = []


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
                self.fields[field].widget.attrs['readonly'] = True
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



class PinboardForm(forms.ModelForm):
    class Meta:
        model = Pinboard
        fields = ['title', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5})
        }

class PinboardCommentForm(forms.ModelForm):
    class Meta:
        model = PinboardComment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows':3, 'cols':50, 'placeholder':'Write your comment here...'})
        }
