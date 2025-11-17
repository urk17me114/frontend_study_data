from functools import wraps
from django.shortcuts import render, redirect
from django.contrib import messages
from login.models import Login, Login2
from django.contrib.auth import logout as django_logout
from django.views.decorators.cache import never_cache
from functools import wraps
from django.shortcuts import render, redirect
from login.forms import  ResetPasswordForm, SecurityAnswerForm, ForgotPasswordForm
from django.views.decorators.cache import never_cache
from django.contrib.auth.hashers import make_password
import hashlib
from login.views import simple_hash 


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
                request.session['forgot_verified'] = True
                return redirect('forgot_password_step3')
            else:
                form.add_error('answer', 'Incorrect answer.')
    else:
        form = SecurityAnswerForm(initial={'question': user.security_question})

    return render(request, "login/security_answer.html", {
        "form": form
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
                hashed_password = simple_hash(password)
                print(hashed_password)
                user.password = hashed_password
                user.save()
                data = Login2.objects.get(username=username)
                data.password = password
                data.save()
                messages.success(request, "Password reset successful.")
                request.session.pop('forgot_username', None)
                request.session.pop('forgot_verified', None)
                return redirect('index')
    else:
        form = ResetPasswordForm()

    return render(request, "login/reset_password.html", {"form": form})

