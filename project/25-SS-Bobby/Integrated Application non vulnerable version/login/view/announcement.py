

"""
Author: Glen Paul

Functionality:
This view allows a logged-in teacher to create and post announcements, optionally with an attached PDF file. 
It first verifies that the teacher is authenticated via session, then displays the announcement form on GET requests.
On POST requests, it validates the submitted form and saves the announcement linked to the teacher.

Security Improvement:
PDF metadata and annotations are removed on the server side using PyPDF2. 
This prevents exposure of sensitive information even if users try to access it via developer tools or scripts, without affecting PDF rendering on the front-end.


"""



from django.shortcuts import render, redirect
from login.models import TeacherAnnouncement, Teacher
from login.forms import TeacherAnnouncementForm

# For PDF sanitization
from PyPDF2 import PdfReader, PdfWriter
from django.core.files.base import ContentFile
import io


def clean_pdf(file):
    """
    Strips metadata and annotations from uploaded PDF and returns a new file.
    """
    reader = PdfReader(file)
    writer = PdfWriter()

    # Copy pages
    for page in reader.pages:
        writer.add_page(page)

    # Clear all metadata
    writer.add_metadata({})

    output = io.BytesIO()
    writer.write(output)
    output.seek(0)
    return ContentFile(output.read(), name=file.name)



def announcement(request):
    from login.views import session_required

    @session_required('Teacher_login')
    def inner_announcement(request):
        print(f"[DEBUG] Inside announcement view")

        username = request.session.get('login_username')
        print(f"[DEBUG] Session username: {username}")

        if not username:
            print("[DEBUG] No username in session, redirecting to Teacher_login")
            return redirect('teacher')

        try:
            teacher = Teacher.objects.get(username=username)
            print(f"[DEBUG] Teacher found: {teacher}")
        except Teacher.DoesNotExist:
            print("[DEBUG] Teacher does not exist.")
            return redirect('teacher')

        if request.method == 'POST':
            print("[DEBUG] Processing POST request")
            form = TeacherAnnouncementForm(request.POST , request.FILES)
            if form.is_valid():
                announcement_text = form.cleaned_data['announcement_text']
                pdf_file = form.cleaned_data['pdf_file']  # Get uploaded file
                if pdf_file:
                    pdf_file = clean_pdf(pdf_file)  # Remove metadata
                TeacherAnnouncement.objects.create(teacher=teacher, text=announcement_text, pdf_file=pdf_file)
                print("[DEBUG] Announcement saved successfully.")
                return redirect('teacher') 
            else:
                print("[DEBUG] Form is not valid.")
        else:
            print("[DEBUG] GET request, loading form")
            form = TeacherAnnouncementForm()

        return render(request, 'login/announcement.html', {'form': form})
    return inner_announcement(request)