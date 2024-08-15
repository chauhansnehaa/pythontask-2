from webbrowser import get
from django.db import models
import pymysql
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core import serializers

conn = pymysql.connect(
        host= "django.cx0u2mm2a511.ap-south-1.rds.amazonaws.com", #endpoint link
        port = 3306, # 3306
        user = 'admin', # admin
        password = 'Rs#R$2020', #adminadmin
        db = 'django', #test
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

    def create_superuser(self, email, first_name, last_name, username, password=None):
        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
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

    @property
    def is_staff(self):
        return self.is_superuser