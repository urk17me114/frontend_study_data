

"""
Author: Glen Paul

Functionality:
This view function, `view_announcement`, is designed to display announcements to students
along with voting information. It retrieves the logged-in student's username from the session,
fetches the corresponding Student object, and queries all TeacherAnnouncements annotated with
the count of upvotes and downvotes. It also fetches the student's existing votes to indicate
their voting status on each announcement. The data is then passed to the 'view_announcement.html'
template for rendering an interactive announcement platform where students can view and vote
on announcements.It serves as a core part of an interactive student announcement and voting feature.
 
"""



from django.shortcuts import render, redirect
from login.models import TeacherAnnouncement, AnnouncementVote, Student
from django.db.models import Count, Q
from login.views import session_required

@session_required('Student_login')
def view_announcement(request):
    username = request.session.get('login_username')
    
    if not username:
        return redirect('login')

    student = Student.objects.get(username=username)

    # Fetch the announcements along with the count of upvotes and downvotes
    announcements = TeacherAnnouncement.objects.annotate(
        upvotes=Count('announcementvote', filter=Q(announcementvote__vote_type='upvote')),
        downvotes=Count('announcementvote', filter=Q(announcementvote__vote_type='downvote'))
    )

    # Fetch the student's votes for each announcement
    student_votes = AnnouncementVote.objects.filter(student=student).values('announcement_id', 'vote_type')

    # Organize the student votes into a dictionary for easy lookup in the template
    student_vote_dict = {vote['announcement_id']: vote['vote_type'] for vote in student_votes}

    # Prepare the vote counts in the correct format
    vote_counts = {
        announcement.id: {
            'upvote': announcement.upvotes,
            'downvote': announcement.downvotes
        }
        for announcement in announcements
    }

    return render(request, 'login/view_announcement.html', {
        'announcements': announcements,
        'student_votes': student_vote_dict,
        'vote_counts': vote_counts  
    })