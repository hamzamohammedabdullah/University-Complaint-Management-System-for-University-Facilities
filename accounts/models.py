from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('staff',   'Facilities Staff'),
        ('admin',   'Administrator'),
    ]
    DEPARTMENT_CHOICES = [
        ('Electrical',        'Electrical'),
        ('Plumbing',          'Plumbing'),
        ('ICT Infrastructure','ICT Infrastructure'),
        ('General Maintenance','General Maintenance'),
        ('Sanitation',        'Sanitation'),
        ('Security',          'Security'),
    ]

    role       = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    student_id = models.CharField(max_length=50, blank=True)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES, blank=True)
    phone      = models.CharField(max_length=20, blank=True)
    is_active  = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"

    @property
    def is_student(self): return self.role == 'student'
    @property
    def is_staff_member(self): return self.role == 'staff'
    @property
    def is_admin(self): return self.role == 'admin'
