
"""
Author: Glen Paul

Functionality:
This function `post_questions` provides students with a platform to post questions.
It ensures that only authenticated students (validated via session) can submit questions.
Currently, it handles form rendering and saving submitted questions to the database.

Motivation:
This functionality is intended as a foundation for a future interactive platform where students
can actively engage by posting questions, fostering communication and collaboration within
the learning environment.
"""



from django.shortcuts import render, redirect
from login.models import Student, Question
from django.shortcuts import get_object_or_404
from login.views import session_required
from login.forms import QuestionForm


@session_required('Student_login')
def post_questions(request):
    username = request.session.get('login_username')
    if not username:
        return redirect('student_login')  # Or show an error page

    student = get_object_or_404(Student, username=username)

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question_text = form.cleaned_data['question_text']
            Question.objects.create(student=student, text=question_text)
            return redirect('student')  # Or redirect to a "thank you" page
    else:
        form = QuestionForm()

    return render(request, 'login/post_question.html', {'form': form})