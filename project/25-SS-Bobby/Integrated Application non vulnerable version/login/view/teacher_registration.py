

"""
Author: Glen Paul

Functionality:
This function handles the teacher registration process, including form submission, CAPTCHA validation, 
and file upload handling.

Security Note:
The CAPTCHA validation has been updated to use Django's built-in `CaptchaField`, which ensures that 
each CAPTCHA can only be solved once and prevents replay attacks. This eliminates the vulnerability 
where an attacker could reuse the same CAPTCHA multiple times to flood the system with fake registrations.
"""




from login.models import  TeacherReg
from django.shortcuts import render, redirect
from django.contrib import messages
from login.forms import TeacherRegistration






def teacher_registration(request):
    if request.method == "POST":      
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
        return render(request, "login/teacherregistration.html", {
        "form": form,
        })