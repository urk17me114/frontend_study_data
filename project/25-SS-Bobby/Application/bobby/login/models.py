from django.db import models

class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    dob = models.DateField()
    gender = models.CharField(max_length=10)
    email = models.EmailField()
    class_applied = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class UserAccount(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    ]
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)  # for simplicity, plaintext here (hash it in production)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username} - {self.role}"
    
class teacher(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    dob = models.DateField()
    gender = models.CharField(max_length=10)
    email = models.EmailField()
    

    def __str__(self):
        return f"{self.first_name} {self.last_name}"