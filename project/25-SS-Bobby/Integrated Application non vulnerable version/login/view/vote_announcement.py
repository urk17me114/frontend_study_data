

"""
Author: Glen Paul

Functionality:
This view function, `vote_announcement`, allows a logged-in student to submit a vote (either 'upvote' or 'downvote')
on a specific announcement via a POST request containing JSON data. It validates the vote type, ensures the student
is authenticated via session, fetches the corresponding Student and TeacherAnnouncement objects, and then records
or updates the vote. If the student has already voted on the announcement, their previous vote will be updated 
instead of creating a duplicate. After saving, it returns the updated counts of upvotes and downvotes for that 
announcement as a JSON response.

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
            existing_vote = AnnouncementVote.objects.filter(
                announcement=announcement,
                student=student
            ).first()
            if existing_vote:
                if existing_vote.vote_type == vote_type:
                    # Already voted same way → do nothing
                    return JsonResponse({
                        'status': 'success',
                        'message': 'Already voted',
                        'upvotes_count': AnnouncementVote.objects.filter(
                            announcement=announcement, vote_type='upvote').count(),
                        'downvotes_count': AnnouncementVote.objects.filter(
                            announcement=announcement, vote_type='downvote').count()
                    })
                else:
                    # Change vote type
                    existing_vote.vote_type = vote_type
                    existing_vote.save()
            else:
                # First time vote
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
