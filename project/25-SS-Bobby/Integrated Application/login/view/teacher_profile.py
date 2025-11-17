"""
=============================================================
 Teacher Profile Feature
=============================================================

Author:
    Thoomu Sai Bhargav

Functionality:
    - Teacher can view/update profile and upload document/photo.
    - Provides a document download endpoint.

Security Notes / Intentional Vulnerabilities (for lab/demo):
    - CSRF disabled on profile + download views (@csrf_exempt).
    - IDOR: allows overriding the target username via query (?username=KP0001).
      This lets an attacker view/update another teacher’s data.

    If you want to FIX later:
      * Remove @csrf_exempt
      * Do NOT allow ?username override; always use session username
      * Validate authorization strictly
=============================================================
"""
import os

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import FileResponse, Http404
from django.views.decorators.csrf import csrf_exempt

from login.views import session_required
from login.models import Login, TeacherReg, Teacher
from login.forms import TeacherProfileForm


@csrf_exempt  #disable CSRF protection
@session_required('Teacher_login')
def teacher_profile(request):
    """
    View/update teacher profile.
    VULNERABLE: Accepts ?username= to choose any teacher (IDOR).
    """
    # VULNERABLE: IDOR (attacker can pass ?username=KP0001 to edit others)
    target_username = request.GET.get('username') or request.session.get('login_username')

    try:
        login_obj = Login.objects.get(username=target_username)
        teacher_reg = TeacherReg.objects.get(email=login_obj.email)
        teacher_model = Teacher.objects.get(username=target_username)
    except (Login.DoesNotExist, TeacherReg.DoesNotExist, Teacher.DoesNotExist):
        messages.error(request, "Teacher data not found.")
        return redirect('teacher')

    if request.method == 'POST':
        form = TeacherProfileForm(request.POST, request.FILES)
        updated_fields = []
        updated_photo = False

        if form.is_valid():
            # Update text fields
            new_firstname = form.cleaned_data.get('firstname')
            new_lastname = form.cleaned_data.get('lastname')

            if new_firstname and new_firstname != teacher_reg.firstname:
                teacher_reg.firstname = new_firstname
                teacher_model.firstname = new_firstname
                updated_fields.append('firstname')

            if new_lastname and new_lastname != teacher_reg.lastname:
                teacher_reg.lastname = new_lastname
                teacher_model.lastname = new_lastname
                updated_fields.append('lastname')

            # Update document if uploaded
            new_document = request.FILES.get('document')
            if new_document:
                try:
                    if teacher_reg.document and os.path.isfile(teacher_reg.document.path):
                        os.remove(teacher_reg.document.path)
                except Exception as e:
                    print(f"Document delete error: {e}")
                teacher_reg.document = new_document
                teacher_model.document = new_document
                updated_fields.append('document')

            # Update profile photo if uploaded
            new_photo = request.FILES.get('profile_photo')
            if new_photo:
                try:
                    if teacher_model.profile_photo and os.path.isfile(teacher_model.profile_photo.path):
                        os.remove(teacher_model.profile_photo.path)
                except Exception as e:
                    print(f"Photo delete error: {e}")
                teacher_model.profile_photo = new_photo
                updated_photo = True

            # Save updates
            if updated_fields:
                teacher_reg.save()  # save fully so document definitely updates
            if updated_fields or updated_photo:
                save_fields = ['firstname', 'lastname', 'document']
                if updated_photo:
                    save_fields.append('profile_photo')
                teacher_model.save(update_fields=save_fields)

            # Feedback
            if updated_fields or updated_photo:
                messages.success(request, "Profile updated successfully.")
            else:
                messages.info(request, "No changes were made.")

            return redirect('teacher_profile')
        else:
            messages.error(request, "Form data invalid.")
            return redirect('teacher_profile')

    else:
        # GET request: populate form
        initial_data = {
            'firstname': teacher_reg.firstname,
            'lastname': teacher_reg.lastname,
            'dob': teacher_reg.dob,
            'gender': teacher_reg.gender,
            'email': teacher_reg.email,
        }
        form = TeacherProfileForm(initial=initial_data)

    return render(request, 'login/teacher_profile.html', {
        'form': form,
        'document_url': teacher_reg.document.url if teacher_reg.document else None,
        'profile_photo': teacher_model.profile_photo.url if teacher_model.profile_photo else None,
    })


@csrf_exempt  # VULNERABLE (CSRF)
@session_required('Teacher_login')
def download_teacher_document(request):
    """
    Download teacher document.
    VULNERABLE: Accepts ?username= to download *any* teacher's document (IDOR).
    """
    # IDOR: attacker can supply ?username=KP0001
    target_username = request.GET.get('username') or request.session.get('login_username')

    try:
        login_obj = Login.objects.get(username=target_username)
        teacher_reg = TeacherReg.objects.get(email=login_obj.email)
        teacher_model = Teacher.objects.get(username=target_username)

        # Prefer TeacherReg, fallback to Teacher
        document_field = teacher_reg.document or teacher_model.document

        if not document_field:
            messages.error(request, "No document uploaded.")
            return redirect('teacher_profile')

        document_path = document_field.path
        if not os.path.exists(document_path):
            messages.error(request, "Document file not found on server.")
            return redirect('teacher_profile')

        return FileResponse(
            open(document_path, 'rb'),
            as_attachment=True,
            filename=os.path.basename(document_path)
        )

    except Login.DoesNotExist:
        messages.error(request, "Invalid teacher username.")
        return redirect('teacher')
    except (TeacherReg.DoesNotExist, Teacher.DoesNotExist):
        messages.error(request, "Teacher record not found.")
        return redirect('teacher')
    except Exception as e:
        print(f"[Download error] {e}")
        raise Http404("Unable to download file.")
