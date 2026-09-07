from django.db import models
from builder_app.models import property_details

# Create your models here.
class booking(models.Model):
    #fields
    user_id=models.CharField(max_length=100)
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    phone=models.CharField(max_length=100)
    property_name=models.CharField(max_length=100)
    property_location=models.CharField(max_length=100)
    property_budget=models.CharField(max_length=100)

class wishlists(models.Model):
    user_id=models.CharField(max_length=100)
    property_photo=models.ImageField()
    property_category=models.CharField(max_length=100)
    property_name=models.CharField(max_length=100)
    property_location=models.CharField(max_length=100)
    property_budget=models.CharField(max_length=100)
    property_bedroom=models.CharField(max_length=100)
    property_bathroom=models.CharField(max_length=100)
    property_area=models.CharField(max_length=100)
    property_floor=models.CharField(max_length=100)
    property_parking=models.CharField(max_length=100)