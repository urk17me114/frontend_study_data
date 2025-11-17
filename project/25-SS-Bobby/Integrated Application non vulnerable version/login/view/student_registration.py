

"""
Author: Glen Paul

Function: student_registration(request)

This function handles student registration via a web form, including CAPTCHA validation
to prevent automated or scripted submissions.

Security Note:
Unlike the earlier version, this implementation uses Django's built-in `CaptchaField`
validation instead of manual checks. This approach ensures that each CAPTCHA is valid
only once and cannot be reused, thereby eliminating replay vulnerabilities.
As a result, attackers cannot bypass CAPTCHA by reusing a previously solved challenge,
which strengthens the form against automated spam registrations and protects data integrity.
"""






from login.models import StudentReg
from django.shortcuts import render, redirect
from django.contrib import messages
from login.forms import StudentRegistration






def student_registration(request):
    
    if request.method == "POST":       
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
        
    return render(request, "login/studentregistration.html", {
        "form": form,
            })