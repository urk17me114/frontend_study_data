
"""
Author: Glen Paul

Functionality:
This view function `student_timetable_view` serves to display the timetable for a logged-in student. 
It uses a session-based decorator to ensure that only authenticated students can access it.

The function:
- Retrieves the current student's username from the session.
- Validates that the username exists; otherwise, it prompts for login.
- Fetches the student record and extracts their class level.
- Queries the timetable entries matching the student's class level.
- Optionally filters timetable entries by a day parameter if provided in the request.
- Optimizes the query with related objects to reduce database hits.
- Renders the timetable along with relevant context data for the frontend display.

"""




from django.shortcuts import render
from login.models import Student, TimetableEntry
from login.models import TimetableEntry
from login.views import session_required



@session_required('Student_login')
def student_timetable_view(request):
    username = request.session.get('login_username', '')  

    
    print(f"[DEBUG] Session username: {username}")  

    
    if not username:
        return render(request, 'login/student.html', {
            'entries': [],
            'error': "User session expired or not logged in.",
        })

    # Get the student and their class level
    try:
        student = Student.objects.get(username=username)
        raw_level = student.classlevel  
        print(f"[DEBUG] Extracted numeric class_level: {raw_level}")
        print(f"[DEBUG] Retrieved class_level from Student: {raw_level}")
    except Student.DoesNotExist:
        return render(request, 'login/student.html', {
            'entries': [],
            'error': "Student not found.",
        })
    

    # Match classlevel to ClassSection.name (e.g., 'Grade 6' matches '6')
    try:
        print(f"[DEBUG] Fetching TimetableEntry for class_section name: '{raw_level}'")
        
        entries = TimetableEntry.objects.filter(class_section__name=raw_level)
        print(f"[DEBUG] Retrieved {entries.count()} timetable entries")
    except Exception as e:
        print(f"[ERROR] Exception occurred during timetable fetch: {e}")
        return render(request, 'login/student.html', {
            'entries': [],
            'error': f"Error loading timetable for class: {raw_level}",
        })

    # Optional: Filter by day if selected
    day = request.GET.get('day')
    if day:
        print(f"[DEBUG] Filtering timetable entries by day: {day}")
        entries = entries.filter(timeslot__day=day)

    # Optimize queries
    entries = entries.select_related('subject', 'teacher', 'room', 'timeslot', 'class_section')

    context = {
        'entries': entries,
        'days': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
        'selected_day': day or '',
        'student_class': raw_level,  # e.g., 'Grade 6'
    }

    return render(request, 'login/student_timetable.html', context)