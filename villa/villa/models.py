from django.db import models

# Create your models here.
class query(models.Model):
    #fields
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    subject=models.CharField(max_length=100)
    message=models.CharField(max_length=1000)

class user_details(models.Model):
    #fields
    photo=models.ImageField()
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    phone=models.CharField(max_length=100)
    password=models.CharField(max_length=100)

class builder_details(models.Model):
    #fields
    buildphoto=models.ImageField()
    buildname=models.CharField(max_length=100)
    buildemail=models.CharField(max_length=100)
    buildphone=models.CharField(max_length=100)
    buildpassword=models.CharField(max_length=100)

class approved_builder_details(models.Model):
    #fields
    buildphoto=models.ImageField()
    buildname=models.CharField(max_length=100)
    buildemail=models.CharField(max_length=100)
    buildphone=models.CharField(max_length=100)
    buildpassword=models.CharField(max_length=100)