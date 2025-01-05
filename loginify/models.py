from django.db import models
from django.utils import timezone

# Create your models here.
class UserDetails(models.Model):
    user_name= models.CharField(max_length=50, primary_key=True)
    email= models.EmailField(unique=True)
    password= models.CharField(max_length=12, blank=True)
    last_login = models.DateTimeField(default=timezone.now)
    