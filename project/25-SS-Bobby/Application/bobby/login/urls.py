from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path("1", views.index ,name="index"),
    path("aaa", views.index2 ,name="index2"),
    path("greet", views.index3 , name = "index3"),
    path("studentregister", views.index4 , name = "index4"),
    path("", views.login_view, name="login"),
    path("adminwelcomepage", views.index5, name="adminwelcomepage"),
    path("createstudentcredentials", views.index6, name='index6'),
    path("createteachercredentials", views.index7, name='index7'),
    path("teacherregister", views.index8 , name = "index8"),
    path("studentwelcomepage", views.index9 , name = "studentwelcomepage"), 
    path("teacherwelcomepage", views.index10 , name = "teacherwelcomepage"),
    #path("edit_student", views.edit_student , name = "edit_student")
    path('students/', views.student_list, name='student_list'),
    path('students/edit/<int:student_id>/', views.edit_student, name='edit_student')




]
