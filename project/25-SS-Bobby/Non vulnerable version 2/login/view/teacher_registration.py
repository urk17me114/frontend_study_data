

"""
Author: Glen Paul

Functionality:
This function handles the teacher registration process, including form submission, CAPTCHA validation, and file upload handling.
It implements a manual CAPTCHA verification that is vulnerable to replay attacks, allowing a hacker to reuse the same CAPTCHA multiple times within a short time window.
Additionally, the file upload validation only checks file extensions and file size, which is a weak security measure and can be bypassed by attackers to upload malicious files.

Motivation of the Vulnerability:
The manual CAPTCHA validation allows CAPTCHA reuse, enabling an attacker to flood the system with multiple fake registrations by replaying the same CAPTCHA.
The weak file type validation increases the risk of malicious file uploads, potentially leading to further exploitation.
These vulnerabilities demonstrate typical security pitfalls in web application form handling that a security-conscious developer should avoid.
"""



import time
from login.models import  TeacherReg
from captcha.fields import CaptchaField
from django.shortcuts import render, redirect
from django.contrib import messages
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from django.core.cache import cache  
from django.http import JsonResponse
from login.view.validate_captcha_manual import validate_captcha_manual
from login.forms import TeacherRegistration




CAPTCHA_REUSE_LIMIT = 10
CAPTCHA_TIME_WINDOW = 20  
FLAG = "FLAG{captcha_reuse_detected}"

def teacher_registration(request):
    if request.method == "POST":
        
        captcha_id = request.POST.get('captcha_0')
        captcha_response = request.POST.get('captcha_1')

        # Manual CAPTCHA check (VULNERABLE: allows reuse)
        if not validate_captcha_manual(captcha_id, captcha_response):
            messages.error(request, "Invalid CAPTCHA.")
            return redirect('teacherregistration')
        

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
        
        
        form = TeacherRegistration(request.POST, request.FILES)
        if form.is_valid():
            firstname = form.cleaned_data['firstname']
            lastname = form.cleaned_data['lastname']
            dob = form.cleaned_data['dob']
            gender = form.cleaned_data['gender']
            email = form.cleaned_data['email']
            document = form.cleaned_data['document']

            teacher = TeacherReg.objects.create(
                firstname=firstname,
                lastname=lastname,
                dob=dob,
                gender=gender,
                email=email
            )

            if document:
                # **Vulnerable File Type Check**
                allowed_extensions = ['.jpg', '.png', '.pdf', '.doc', '.docx', '.jpeg']
                max_file_size = 7 * 1024 * 1024  # 7 MB in bytes

                if not any(document.name.endswith(ext) for ext in allowed_extensions):
                    messages.error(request, "Invalid file type. Only .jpg, .png, .pdf, .doc, .docx, .jpeg files are allowed.")
                    return redirect('teacherregistration')
                
                    
                
                if document.size > max_file_size:
                    messages.error(request, "File size exceeds the maximum limit of 7 MB.")
                    return redirect('teacherregistration')
                
                else:
                    teacher.document = document
                    teacher.save()

            messages.success(request, "Teacher registered successfully!")
            return redirect('index')
    else:
        form = TeacherRegistration()
        new_captcha = CaptchaStore.generate_key()
        captcha_image = captcha_image_url(new_captcha)
        return render(request, "login/teacherregistration.html", {
        "form": form,
        "captcha_key": new_captcha,
        "captcha_image_url": captcha_image
    })