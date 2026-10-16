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

    # Phase 3 Enhancements: Floor Plan & Location Intelligence
    floor_plan_image=models.ImageField(upload_to='floor_plans/', null=True, blank=True)
    hospital_dist=models.CharField(max_length=50, default='1.5 km', blank=True)
    pharmacy_dist=models.CharField(max_length=50, default='0.5 km', blank=True)
    school_dist=models.CharField(max_length=50, default='2.0 km', blank=True)
    supermarket_dist=models.CharField(max_length=50, default='1.2 km', blank=True)
    bank_dist=models.CharField(max_length=50, default='1.0 km', blank=True)
    bus_stop_dist=models.CharField(max_length=50, default='0.4 km', blank=True)
    railway_dist=models.CharField(max_length=50, default='3.5 km', blank=True)
    airport_dist=models.CharField(max_length=50, default='22 km', blank=True)
    main_road_dist=models.CharField(max_length=50, default='0.3 km', blank=True)
    # Phase 4 Enhancements: Interactive 3D Model
    model_3d=models.FileField(upload_to='models_3d/', null=True, blank=True)
    latitude=models.FloatField(null=True, blank=True)
    longitude=models.FloatField(null=True, blank=True)