from django.db import models

# Create your models here.
class query(models.Model):
    #fields
    user_id = models.CharField(max_length=100, default='', blank=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    subject = models.CharField(max_length=200, default='General Inquiry', blank=True)
    message = models.TextField(default='', blank=True)
    problem_type = models.CharField(max_length=200, default='', blank=True)
    rating = models.CharField(max_length=20, default='', blank=True)
    status = models.CharField(max_length=50, default='New')
    resolution_details = models.TextField(default='', blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

class user_details(models.Model):
    #fields
    photo = models.ImageField()
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

class builder_details(models.Model):
    #fields
    buildphoto = models.ImageField()
    buildname = models.CharField(max_length=100)
    buildemail = models.CharField(max_length=100)
    buildphone = models.CharField(max_length=100)
    buildpassword = models.CharField(max_length=100)

class approved_builder_details(models.Model):
    #fields
    buildphoto = models.ImageField()
    buildname = models.CharField(max_length=100)
    buildemail = models.CharField(max_length=100)
    buildphone = models.CharField(max_length=100)
    buildpassword = models.CharField(max_length=100)