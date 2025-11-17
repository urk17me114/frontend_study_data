

"""
Author: Glen Paul

Functionality:
This view allows a logged-in teacher to create and post announcements, optionally with an attached PDF file. 
It first verifies that the teacher is authenticated via session, then displays the announcement form on GET requests.
On POST requests, it validates the submitted form and saves the announcement linked to the teacher.

Vulnerability:
Uploaded PDFs are stored and served without removing metadata or annotations. 
This allows a malicious user or student to access sensitive information, such as document metadata or embedded comments, 
via browser developer tools or scripts (e.g., using PDF.js), potentially exposing confidential data.


"""



from django.shortcuts import render, redirect
from login.models import TeacherAnnouncement, Teacher
from login.forms import TeacherAnnouncementForm



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