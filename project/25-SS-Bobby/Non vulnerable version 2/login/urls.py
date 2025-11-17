from django.contrib import admin
from django.urls import path
from . import views
import login.view.timetable as timetable
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from login.view import forgot_password, dashboard, marks, login, search, password, assignment
from django.conf.urls import handler400, handler403, handler404, handler500
from login.view import error_views
from login.view import forgot_password, dashboard, marks, login, search, password
from login.view.student_timetable_view import student_timetable_view
from login.view.student_registration import student_registration
from login.view.teacher_registration import teacher_registration
from login.view.post_questions import post_questions
from login.view.announcement import announcement
from login.view.view_announcement import view_announcement
from login.view.vote_announcement import vote_announcement


urlpatterns=[
    path("", login.index, name="index"),
    #path("greet", views.greet, name="greet"),
    #path('dashboard/', views.dashboard, name='dashboard'),
    path("admin/registration", views.registration, name="registration"),
    #path("teacher/add_marks", views.add_marks, name="add_marks"),
    path("student/view_marks", marks.view_marks, name="view_marks"),
    path("logout/", login.logout_view, name="logout"),
    path('captcha/', include('captcha.urls')),
    path("studentregistration", student_registration, name="studentregistration"),
    path("teacherregistration", teacher_registration, name="teacherregistration"),
    path('admin/', dashboard.admin_dashboard, name='admin'),
    path('teacher/', dashboard.teacher_dashboard, name='teacher'),
    path('student/', dashboard.student_dashboard, name='student'),
    path('add-marks/', marks.add_marks_step1, name='add_marks_step1'),
    path('add-marks/students/', marks.add_marks_step2, name='add_marks_step2'),
    path('change-password/', password.change_password, name='change_password'),
    path('forgot_password/', forgot_password.forgot_password_step1, name='forgot_password_step1'),
    path('forgot_password/step2/', forgot_password.forgot_password_step2, name='forgot_password_step2'),
    path('forgot_password/step3/', forgot_password.forgot_password_step3, name='forgot_password_step3'),
    path('security_question/', password.security_question, name='security_question'),
    path('search/', search.search_student, name='search_student'),
    path('search-teacher/', search.search_teacher, name='search_teacher'),
    path("studentapplication", views.student_application_view, name="studentapplication"),
    path('student-approval/', views.student_approval, name='student_approval'),
    path('teacher-approval/', views.teacher_approval, name='teacher_approval'),
    path('approve-student/<int:student_id>/', views.approve_student, name='approve_student'),
    path('reject-student/<int:student_id>/', views.reject_student, name='reject_student'),
    path('approve-teacher/<int:teacher_id>/', views.approve_teacher, name='approve_teacher'),
    path('reject-teacher/<int:teacher_id>/', views.reject_teacher, name='reject_teacher'),
    path('student/profile/', views.student_profile, name='student_profile'),
    path('teacher/profile/', views.teacher_profile, name='teacher_profile'),
    path('login/teacher/download_document/', views.download_teacher_document, name='download_teacher_document'),
    path('admin/profile/', views.admin_profile, name='admin_profile'),
    path('admin/create_timetable', timetable.create_timetable, name='create_timetable'),
    path('admin/add_subject/', timetable.add_subject, name='add_subject'),
    path('admin/add_teacher/', timetable.add_teacher, name='add_teacher'),
    path('admin/add_classsection/', timetable.add_classsection, name='add_classsection'),
    path('admin/add_room/', timetable.add_room, name='add_room'),
    path('admin/add_timeslot/', timetable.add_timeslot, name='add_timeslot'),
    path('admin/generate_timetable/', timetable.generate_timetable_view, name='generate_timetable'),
    #path('admin/timetable/', views.timetable_view, name='timetable'),
    path('admin/timetable/', timetable.admin_timetable_view, name='admin_timetable'),
    path('teacher/timetable/', timetable.teacher_timetable_view, name='teacher_timetable'),
    path('view-logs', login.view_logs, name='view_logs'),
    path('student_timetable/', student_timetable_view, name='student_timetable'),
    path('post_question/', post_questions, name='post_question'),
    path('announcement/', announcement, name='announcement'),
    path('view_announcement/', view_announcement, name='view_announcement'),
    path('vote_announcement/', vote_announcement, name='vote_announcement'),
    path('student/set_sid_from_storage/', marks.set_sid_from_storage, name='set_sid_from_storage'),
    path('teacher/questions/new/', assignment.teacher_create_question, name='teacher_create_question'),
    path('teacher/questions/', assignment.teacher_questions_list, name='teacher_questions_list'),
    path('teacher/review/', assignment.teacher_review_submissions, name='teacher_review_submissions'),
    path('teacher/review/<int:submission_id>/seen/', assignment.teacher_mark_seen, name='teacher_mark_seen'),
    path('teacher/review/<int:submission_id>/grade/', assignment.teacher_grade_submission, name='teacher_grade_submission'),
    path('student/questions/', assignment.student_questions_list, name='student_questions_list'),
    path('student/questions/<int:question_id>/submit/', assignment.student_submit_for_question, name='student_submit_for_question'),
    path('student/submissions/', assignment.student_my_submissions, name='student_my_submissions'),
]
   



# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler400 = error_views.custom_bad_request_view
handler403 = error_views.custom_permission_denied_view
handler404 = error_views.custom_page_not_found_view
handler500 = error_views.custom_server_error_view
