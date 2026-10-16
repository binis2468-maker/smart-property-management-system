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

class property_review(models.Model):
    user_id=models.CharField(max_length=100)
    user_name=models.CharField(max_length=100)
    property_id=models.IntegerField()
    rating=models.IntegerField(default=5)
    comment=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

class property_visit(models.Model):
    user_id = models.CharField(max_length=100)
    user_name = models.CharField(max_length=100)
    user_email = models.CharField(max_length=100)
    user_phone = models.CharField(max_length=100)
    builder_id = models.CharField(max_length=100)
    property_id = models.IntegerField(default=0)
    property_name = models.CharField(max_length=100)
    property_location = models.CharField(max_length=100)
    property_budget = models.CharField(max_length=100)
    visit_date = models.DateField()
    time_slot = models.CharField(max_length=100)
    status = models.CharField(max_length=50, default='Pending') # Pending, Confirmed, Rejected, Rescheduled
    suggested_time = models.CharField(max_length=200, default='', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class chat_conversation(models.Model):
    user_id = models.CharField(max_length=100)
    user_name = models.CharField(max_length=100, default='')
    builder_id = models.CharField(max_length=100)
    builder_name = models.CharField(max_length=100, default='')
    property_id = models.IntegerField(default=0)
    property_name = models.CharField(max_length=100, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class chat_message(models.Model):
    conversation = models.ForeignKey(chat_conversation, on_delete=models.CASCADE, related_name='messages')
    sender_type = models.CharField(max_length=20) # 'user' or 'builder'
    sender_id = models.CharField(max_length=100)
    receiver_type = models.CharField(max_length=20) # 'user' or 'builder'
    receiver_id = models.CharField(max_length=100)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

class notification(models.Model):
    recipient_type = models.CharField(max_length=20) # 'user', 'builder', 'admin'
    recipient_id = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    message = models.TextField()
    link = models.CharField(max_length=200, default='', blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class property_booking(models.Model):
    user_id = models.CharField(max_length=100)
    user_name = models.CharField(max_length=100)
    user_email = models.CharField(max_length=100)
    user_phone = models.CharField(max_length=100)
    builder_id = models.CharField(max_length=100)
    property_id = models.IntegerField()
    property_name = models.CharField(max_length=100)
    property_location = models.CharField(max_length=100)
    property_price = models.FloatField(default=0.0)
    advance_amount = models.FloatField(default=0.0)
    remaining_amount = models.FloatField(default=0.0)
    booking_status = models.CharField(max_length=50, default='Requested') # Requested, Approved, Payment Pending, Confirmed, Rejected, Cancelled
    advance_payment_status = models.CharField(max_length=50, default='Pending') # Pending, Successful, Failed
    transaction_id = models.CharField(max_length=100, default='', blank=True)
    payment_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class payment_transaction(models.Model):
    booking = models.ForeignKey(property_booking, on_delete=models.CASCADE, related_name='payments')
    user_id = models.CharField(max_length=100)
    builder_id = models.CharField(max_length=100)
    property_name = models.CharField(max_length=100)
    amount = models.FloatField()
    payment_status = models.CharField(max_length=50, default='Successful')
    transaction_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100, default='Test Sandbox Gateway')
    created_at = models.DateTimeField(auto_now_add=True)
