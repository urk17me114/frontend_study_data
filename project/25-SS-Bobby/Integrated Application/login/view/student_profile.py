"""
=============================================================
 Student Profile Feature
=============================================================

Author:
    Thoomu Sai Bhargav

Functionality:
    - Student can view/update profile (mirrors Student + StudentApplication fields).
    - Photo upload supported.

Security Notes / Potential Vulnerabilities:
    - Requires Student session via session_required('Student_login').
    - Ensure file storage safe; templates must escape text fields.
=============================================================
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404

from login.views import session_required
from login.models import Login, Student, StudentApplication
from login.forms import StudentProfileForm


@session_required('Student_login')
def student_profile(request):
    """
    Allow logged-in student to view and update their profile.
    """
    username = request.session.get('login_username')

    try:
        login_obj = Login.objects.get(username=username)
        student_app = StudentApplication.objects.get(student_email=login_obj.email)
        student_model = Student.objects.get(username=username)
    except (Login.DoesNotExist, StudentApplication.DoesNotExist, Student.DoesNotExist):
        messages.error(request, "Student data not found.")
        return redirect('student')

    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            new_photo = cleaned_data.get('profile_photo')
            # Track changes to update selectively

            update_student_fields = {}
            update_app_fields = {}

            for field, value in cleaned_data.items():
                if field in form.readonly_fields or field == 'profile_photo':
                    continue

                if hasattr(student_model, field) and getattr(student_model, field) != value:
                    update_student_fields[field] = value

                if hasattr(student_app, field) and getattr(student_app, field) != value:
                    update_app_fields[field] = value

            # Save photo if uploaded
            if new_photo:
                student_model.profile_photo = new_photo

            # Only save student_model if there are actual changes
            fields_to_update = list(update_student_fields.keys())
            if new_photo:
                fields_to_update.append('profile_photo')

            if fields_to_update:
                for field, value in update_student_fields.items():
                    setattr(student_model, field, value)
                student_model.save(update_fields=fields_to_update)

            # Update StudentApplication if needed
            if update_app_fields:
                StudentApplication.objects.filter(pk=student_app.pk).update(**update_app_fields)

            messages.success(request, "Profile updated successfully.")
            return redirect('student_profile')
    else:
        # Initial data from StudentApplication
        # Preload initial values from StudentApplication
        initial_data = {
            field: getattr(student_app, field)
            for field in StudentProfileForm.base_fields
            if hasattr(student_app, field)
        }
        form = StudentProfileForm(initial=initial_data)

    return render(request, 'login/student_profile.html', {
        'form': form,
        'profile_photo': student_model.profile_photo,
    })