

"""
Author: Glen Paul

Functionality:
This view function, `vote_announcement`, allows a logged-in student to submit a vote (either 'upvote' or 'downvote')
on a specific announcement via a POST request containing JSON data. It validates the vote type, ensures the student
is authenticated via session, fetches the corresponding Student and TeacherAnnouncement objects, and then records
the vote. After saving, it returns the updated counts of upvotes and downvotes for that announcement as a JSON response.

Motivation of the Vulnerability:
This function currently does not prevent multiple votes by the same student on the same announcement,
allowing a user to cast repeated votes which can skew the vote counts unfairly. This vulnerability could
be exploited to manipulate the perceived popularity or importance of announcements. The motivation behind
highlighting this vulnerability is to encourage implementing protections such as checking for existing votes
by the same student before creating a new one, or allowing vote updates instead of duplicates.
"""



import json
from django.http import JsonResponse
from login.models import AnnouncementVote, TeacherAnnouncement, Student
from django.http import JsonResponse
from login.views import session_required



@session_required('Student_login')
def vote_announcement(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            announcement_id = data.get('announcement_id')
            vote_type = data.get('vote_type')

            if vote_type not in ['upvote', 'downvote']:
                return JsonResponse({'status': 'error', 'message': 'Invalid vote type'})

           
            username = request.session.get('login_username')
            if not username:
                return JsonResponse({'status': 'error', 'message': 'User not logged in'})

            
            student = Student.objects.get(username=username)

            
            announcement = TeacherAnnouncement.objects.get(id=announcement_id)

            # To handle vote
            
            AnnouncementVote.objects.create(
                    announcement=announcement,
                    student=student,
                    vote_type=vote_type
                )

            # Return updated counts
            upvotes_count = AnnouncementVote.objects.filter(announcement=announcement, vote_type='upvote').count()
            downvotes_count = AnnouncementVote.objects.filter(announcement=announcement, vote_type='downvote').count()

            return JsonResponse({
                'status': 'success',
                'message': 'Vote registered successfully',
                'upvotes_count': upvotes_count,
                'downvotes_count': downvotes_count
            })

        except Student.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Student not found'})

        except TeacherAnnouncement.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Announcement not found'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
