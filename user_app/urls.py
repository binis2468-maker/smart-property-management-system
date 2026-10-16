"""
URL configuration for villa project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('viewprop', views.viewprop, name='viewprop'),
    path('schedulevisit/<int:id>', views.schedulevisit, name='schedulevisit'),
    path('wishlist/<int:id>', views.wishlist, name='wishlist'),
    path('add_review/<int:id>', views.add_review, name='add_review'),
    
    # Phase 2 Routes
    path('check_availability/<int:id>', views.check_availability, name='check_availability'),
    path('schedulevisit_slot/<int:id>', views.schedulevisit_slot, name='schedulevisit_slot'),
    path('my_visits', views.my_visits, name='my_visits'),
    path('respond_visit/<int:id>/<str:action>', views.respond_visit, name='respond_visit'),
    path('confirm_rescheduled_visit/<int:id>', views.confirm_rescheduled_visit, name='confirm_rescheduled_visit'),
    
    path('start_chat/<str:builder_id>/<int:property_id>', views.start_chat, name='start_chat'),
    path('chat_list', views.chat_list, name='chat_list'),
    path('chat_detail/<int:conv_id>', views.chat_detail, name='chat_detail'),
    path('send_chat_message/<int:conv_id>', views.send_chat_message, name='send_chat_message'),
    
    path('notifications', views.notifications_list, name='notifications'),
    path('mark_notification_read/<int:id>', views.mark_notification_read, name='mark_notification_read'),
    
    path('request_booking/<int:property_id>', views.request_booking, name='request_booking'),
    path('my_bookings', views.my_bookings, name='my_bookings'),
    path('manage_booking_request/<int:booking_id>/<str:action>', views.manage_booking_request, name='manage_booking_request'),
    path('pay_advance/<int:booking_id>', views.pay_advance, name='pay_advance'),
    path('process_sandbox_payment/<int:booking_id>', views.process_sandbox_payment, name='process_sandbox_payment'),
    path('report_issue', views.report_issue, name='report_issue'),
    path('property_details/<int:id>', views.property_detail_view, name='property_details'),
]

