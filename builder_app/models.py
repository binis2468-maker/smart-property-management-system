from django.db import models

# Create your models here.
class property_details(models.Model):
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