from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    
class ChangePwd(models.Model):
    existingPassword = models.CharField(max_length=50)
    newPassword = models.CharField(max_length=50)