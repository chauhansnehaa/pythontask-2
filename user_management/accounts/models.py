from webbrowser import get
from django.db import models
import pymysql
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core import serializers
from django.conf import settings
from django.urls import reverse
from datetime import datetime, date


conn = pymysql.connect(
        host= "django.cx0u2mm2a511.ap-south-1.rds.amazonaws.com", 
        port = 3306,
        user = 'admin', 
        password = 'Rs#R$2020',
        db = 'django', 
        )



class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            username=username,
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user

   

class CustomUser(AbstractBaseUser):
    USER_TYPE_CHOICES = (
        ('Doctor', 'Doctor'),
        ('Patient', 'Patient'),
    )

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default.jpg')
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    address_line1 = models.CharField(max_length=100, default='Unknown')
    city = models.CharField(max_length=50, default='Unknown')
    state = models.CharField(max_length=50, default='Unknown')
    pincode = models.CharField(max_length=10, default='Unknown')
    user_type = models.CharField(max_length=10, choices=[('Doctor', 'Doctor'), ('Patient', 'Patient')])
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('doctor-dashboard')


class Post(models.Model):

    DRAFT = 'Draft'
    PUBLISHED = 'Published'
    STATUS_CHOICES = [
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published'),
    ]
    title = models.CharField(max_length=255)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    BlogImage = models.ImageField(upload_to='blog_pics/', default='default.jpg')
    category = models.CharField(max_length=255,default='select')
    summary = models.TextField(max_length=255,default='Add summary')
    content = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=DRAFT)
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.title} | {self.author.username}"
    def get_absolute_url(self):
            return reverse('article-detail', args=[self.pk])
