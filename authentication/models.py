from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import UserManager

class User(AbstractBaseUser, PermissionsMixin):
  
  # required fields for registration
  first_name = models.CharField(max_length = 100)
  last_name = models.CharField(max_length = 100)
  email = models.EmailField(unique = True)
  password = models.CharField(max_length = 100)
  
  # fields for superadmin 
  is_active = models.BooleanField(default = True)
  is_staff = models.BooleanField(default = False)
  is_superuser = models.BooleanField(default = False)
  
  created_at = models.DateTimeField(auto_now_add = True)
  updated_at = models.DateTimeField(auto_now = True)
  last_login = models.DateTimeField(auto_now = True)
  
  USERNAME_FIELD = 'email' # field to use for login
  REQUIRED_FIELDS = []
  
  objects = UserManager()
  
  def __str__(self):
    return f"{self.email} "
  
  
class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
  points = models.PositiveIntegerField(default=0)
  level = models.PositiveIntegerField(default=0)
  streak = models.IntegerField(default=0)
  highest_streak = models.IntegerField(default=0) 
  
  updated_at = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return f"{self.user.first_name} {self.user.last_name}'s Profile"
  
  
  
  
  
  
  