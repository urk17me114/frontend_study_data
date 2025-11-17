from django.contrib import admin
from django.urls import path
from . import views
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    path("", views.index, name="index"),
    #path("greet", views.greet, name="greet"),
    #path('dashboard/', views.dashboard, name='dashboard'),
    path("admin/registration", views.registration, name="registration"),
    path("teacher/add_marks", views.add_marks, name="add_marks"),
    path("student/view_marks", views.view_marks, name="view_marks"),
    path("logout/", views.logout_view, name="logout"),
    path('captcha/', include('captcha.urls')),
    path("studentregistration", views.student_registration, name="studentregistration"),
    path("teacherregistration", views.teacher_registration, name="teacherregistration"),
    path('admin/', views.admin_dashboard, name='admin'),
    path('teacher/', views.teacher_dashboard, name='teacher'),
    path('student/', views.student_dashboard, name='student'),
    path('change-password/', views.change_password, name='change_password'),
    path('forgot_password/', views.forgot_password_step1, name='forgot_password_step1'),
    path('forgot_password/step2/', views.forgot_password_step2, name='forgot_password_step2'),
    path('forgot_password/step3/', views.forgot_password_step3, name='forgot_password_step3'),
    path('security_question/', views.security_question, name='security_question'),
    path('admin/search/', views.search_student, name='search_student'),
    path("studentapplication", views.student_application_view, name="studentapplication"),
    path('student-approval/', views.student_approval, name='student_approval'),
    path('teacher-approval/', views.teacher_approval, name='teacher_approval'),
    path('approve-student/<int:student_id>/', views.approve_student, name='approve_student'),
    path('reject-student/<int:student_id>/', views.reject_student, name='reject_student'),
    path('approve-teacher/<int:teacher_id>/', views.approve_teacher, name='approve_teacher'),
    path('reject-teacher/<int:teacher_id>/', views.reject_teacher, name='reject_teacher'),

    
]


# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
