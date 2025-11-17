"""
=============================================================
 Assignment Management 
=============================================================

Author:
    Arundas Mohandas 
    Ganga Sunil

Functionality:
    Provides functionality for teachers and students to manage assignments:
        Teachers can create questions, review submissions and grade them.
        Students can view questions for their class and subjects, submit assignments and track their own submissions.

Vulnerability:
    This makes the application uses vulnerable to XML External Entity (XXE) attacks with denial of service using Billion Laughs.  
    A student could upload an XML that references sensitive server files or external URLs.  

=============================================================
"""

from functools import wraps
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from django.views.decorators.cache import never_cache
import tempfile
import io
import contextlib
from lxml import etree

from login.models import (
    Student, TeacherAvailability, ClassSection, Subject,
    AssignmentQuestion, AssignmentSubmission
)
from login.forms import (
    AssignmentQuestionForm, AssignmentSubmissionForm,
    GradeSubmissionForm, SubmissionFilterForm
)


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


# ------------------------
# Vulnerable XML parser
# ------------------------
def parse_xml(file_path):
    parser = etree.XMLParser(load_dtd=True, resolve_entities=True)
    with open(file_path, 'rb') as f:
        tree = etree.parse(f, parser)
        print(etree.tostring(tree))


# ============================================================
# TEACHER: Create question
# ============================================================
@session_required('Teacher_login')
def teacher_create_question(request):
    username = request.session.get('login_username')
    teacher = get_object_or_404(TeacherAvailability, username=username)

    if request.method == 'POST':
        form = AssignmentQuestionForm(request.POST, request.FILES)
        if form.is_valid():
            q = form.save(commit=False)
            if q.subject not in teacher.subjects.all() or q.class_section not in teacher.class_sections.all():
                messages.error(request, "You can only post questions for your own subjects and class sections.")
                return redirect('teacher_create_question')
            q.teacher_username = teacher.username
            q.save()
            messages.success(request, "Question posted.")
            return redirect('teacher_questions_list')
    else:
        form = AssignmentQuestionForm()
        form.fields['subject'].queryset = teacher.subjects.all()
        form.fields['class_section'].queryset = teacher.class_sections.all()

    return render(request, 'login/teacher_create_question.html', {'form': form})


# ============================================================
# TEACHER: List own posted questions
# ============================================================
@session_required('Teacher_login')
def teacher_questions_list(request):
    username = request.session.get('login_username')
    teacher = get_object_or_404(TeacherAvailability, username=username)
    questions = AssignmentQuestion.objects.filter(
        teacher_username=teacher.username
    ).order_by('-created_at')
    return render(request, 'login/teacher_questions_list.html', {'questions': questions})


# ============================================================
# STUDENT: List questions for my class/subjects
# ============================================================
@session_required('Student_login')
def student_questions_list(request):
    student_username = request.session.get('student_username') or request.session.get('login_username')
    request.session['student_username'] = student_username
    student = get_object_or_404(Student, username=student_username)

    class_section = get_object_or_404(ClassSection, name=student.classlevel)
    qs = AssignmentQuestion.objects.filter(class_section=class_section).order_by('-created_at')

    sel_subject_id = request.GET.get('subject')
    if sel_subject_id:
        qs = qs.filter(subject_id=sel_subject_id)

    subjects = Subject.objects.filter(id__in=qs.values_list('subject_id', flat=True).distinct())
    now = timezone.now()

    return render(request, 'login/student_questions_list.html', {
        'questions': qs,
        'subjects': subjects,
        'selected_subject': sel_subject_id,
        'now': now,
    })


# ============================================================
# STUDENT: Submit assignment for a question
# ============================================================
@session_required('Student_login')
def student_submit_for_question(request, question_id):
    student_username = request.session.get('student_username') or request.session.get('login_username')
    request.session['student_username'] = student_username
    student = get_object_or_404(Student, username=student_username)

    question = get_object_or_404(AssignmentQuestion, id=question_id)

    class_section = get_object_or_404(ClassSection, name=student.classlevel)
    if question.class_section_id != class_section.id:
        messages.error(request, "This question is not assigned to your class.")
        return redirect('student_questions_list')

    try:
        instance = AssignmentSubmission.objects.get(question=question, student=student)
    except AssignmentSubmission.DoesNotExist:
        instance = None

    if request.method == 'POST':
        data = request.POST.copy()

        xml_file = request.FILES.get('assignment_xml')
        if xml_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".xml") as tmp:
                for chunk in xml_file.chunks():
                    tmp.write(chunk)
                tmp_path = tmp.name

            try:
                buf = io.StringIO()
                with contextlib.redirect_stdout(buf):
                    parse_xml(tmp_path)
                printed_xml = buf.getvalue()

                parser = etree.XMLParser(load_dtd=True, resolve_entities=True)
                tree = etree.parse(tmp_path, parser)
                root = tree.getroot()

                if root.findtext("text_content"):
                    data["text_content"] = root.findtext("text_content")

            except Exception as e:
                messages.error(request, f"XML parsing failed: {e}")
                return redirect('student_submit_for_question', question_id=question_id)

        form = AssignmentSubmissionForm(data, request.FILES, instance=instance)
        if form.is_valid():
            sub = form.save(commit=False)
            sub.question = question
            sub.student = student
            sub.status = 'submitted'
            sub.save()
            messages.success(request, "Assignment submitted.")
            return redirect('student_my_submissions')
    else:
        form = AssignmentSubmissionForm(instance=instance)

    return render(request, 'login/student_submit_for_question.html', {
        'question': question,
        'form': form,
        'existing_submission': instance
    })


# ============================================================
# STUDENT: View my submissions + status/marks
# ============================================================
@session_required('Student_login')
def student_my_submissions(request):
    student_username = request.session.get('student_username') or request.session.get('login_username')
    request.session['student_username'] = student_username
    student = get_object_or_404(Student, username=student_username)

    subs = AssignmentSubmission.objects.filter(student=student).select_related(
        'question', 'question__subject', 'question__class_section'
    ).order_by('-submitted_at')

    return render(request, 'login/student_my_submissions.html', {'submissions': subs})


# ============================================================
# TEACHER: Review submissions (filter + scope)
# ============================================================
@session_required('Teacher_login')
def teacher_review_submissions(request):
    username = request.session.get('login_username')
    teacher = get_object_or_404(TeacherAvailability, username=username)

    qs = AssignmentSubmission.objects.filter(
        Q(question__teacher_username=teacher.username) |
        (Q(question__subject__in=teacher.subjects.all()) & Q(question__class_section__in=teacher.class_sections.all()))
    ).select_related('question', 'student', 'question__subject', 'question__class_section')

    form = SubmissionFilterForm(request.GET or None, teacher=teacher)
    if form.is_valid():
        if form.cleaned_data.get('subject'):
            qs = qs.filter(question__subject=form.cleaned_data['subject'])
        if form.cleaned_data.get('class_section'):
            qs = qs.filter(question__class_section=form.cleaned_data['class_section'])
        if form.cleaned_data.get('status'):
            qs = qs.filter(status=form.cleaned_data['status'])

    sort = request.GET.get('sort')
    qs = qs.order_by('submitted_at' if sort == 'oldest' else '-submitted_at')

    return render(request, 'login/teacher_review_submissions.html', {
        'submissions': qs,
        'form': form
    })


# ============================================================
# TEACHER: Mark seen
# ============================================================
@session_required('Teacher_login')
def teacher_mark_seen(request, submission_id):
    username = request.session.get('login_username')
    teacher = get_object_or_404(TeacherAvailability, username=username)

    sub = get_object_or_404(AssignmentSubmission, id=submission_id)

    if not (
        sub.question.teacher_username == teacher.username or
        (sub.question.subject in teacher.subjects.all() and sub.question.class_section in teacher.class_sections.all())
    ):
        messages.error(request, "Not authorized for this submission.")
        return redirect('teacher_review_submissions')

    sub.status = 'seen'
    sub.save()
    messages.success(request, "Marked as seen.")
    return redirect('teacher_review_submissions')


# ============================================================
# TEACHER: Grade a submission
# ============================================================
@session_required('Teacher_login')
def teacher_grade_submission(request, submission_id):
    username = request.session.get('login_username')
    teacher = get_object_or_404(TeacherAvailability, username=username)

    sub = get_object_or_404(AssignmentSubmission, id=submission_id)

    if not (
        sub.question.teacher_username == teacher.username or
        (sub.question.subject in teacher.subjects.all() and sub.question.class_section in teacher.class_sections.all())
    ):
        messages.error(request, "Not authorized for this submission.")
        return redirect('teacher_review_submissions')

    if request.method == 'POST':
        form = GradeSubmissionForm(request.POST, instance=sub)
        if form.is_valid():
            graded = form.save(commit=False)
            graded.status = 'graded'
            graded.save()
            messages.success(request, "Marks saved and returned to student.")
            return redirect('teacher_review_submissions')
    else:
        form = GradeSubmissionForm(instance=sub)

    return render(request, 'login/teacher_grade_submission.html', {
        'submission': sub,
        'form': form
    })
