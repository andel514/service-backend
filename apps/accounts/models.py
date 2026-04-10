from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

class User(AbstractUser):
    ROLE_CHOICES = (
        ('candidate', 'Исполнитель'),
        ('employer', 'Работодатель'),
    )
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$')
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    phone_number = models.CharField(validators=[phone_regex], max_length=17, unique=True)
    city = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_number', 'city', 'role']
    
    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"