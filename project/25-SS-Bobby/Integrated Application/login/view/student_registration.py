

"""
Author: Glen Paul

Function: student_registration(request)

This function handles student registration via a web form, including CAPTCHA validation to prevent automated submissions.

Motivation / Vulnerability:
The CAPTCHA validation implemented here is intentionally vulnerable to replay attacks.
It allows the reuse of the same CAPTCHA token multiple times within a short time window,
which enables attackers to bypass the CAPTCHA protection by reusing a previously valid CAPTCHA response.

By exploiting this vulnerability, a hacker can bypass the CAPTCHA and flood the database with fake or spam student registration data,
potentially leading to data integrity issues and resource exhaustion.

"""




import time
from login.models import StudentReg
from captcha.fields import CaptchaField
from django.shortcuts import render, redirect
from django.contrib import messages
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from django.core.cache import cache 
from django.http import JsonResponse
from login.forms import StudentRegistration
from login.view.validate_captcha_manual import validate_captcha_manual


CAPTCHA_REUSE_LIMIT = 10
CAPTCHA_TIME_WINDOW = 20  
FLAG = "FLAG{captcha_reuse_detected}"


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