from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Avg, Count, Q
from django.utils import timezone
from datetime import date, datetime
import re
import random

from builder_app.models import property_details
from villa.models import user_details, approved_builder_details, query
from user_app.models import (
    booking, wishlists, property_review, property_visit,
    chat_conversation, chat_message, notification,
    property_booking, payment_transaction
)

# Helper function to send notification safely
def send_notification(recipient_type, recipient_id, title, message, link=''):
    notification.objects.create(
        recipient_type=recipient_type,
        recipient_id=str(recipient_id),
        title=title,
        message=message,
        link=link
    )

# -------------------------------------------------------------
# 1. PROPERTY CATALOG & SEARCH
# -------------------------------------------------------------
def viewprop(request):
    queryset = property_details.objects.all().order_by('-id')
    
    category = request.GET.get('category', '').strip()
    keyword = request.GET.get('keyword', '').strip()
    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()
    bedrooms = request.GET.get('bedrooms', '').strip()

    if category and category.lower() != 'all':
        queryset = queryset.filter(property_category__icontains=category)
        
    if keyword:
        queryset = queryset.filter(
            Q(property_name__icontains=keyword) |
            Q(property_location__icontains=keyword)
        )

    if bedrooms and bedrooms.isdigit():
        queryset = queryset.filter(property_bedroom__gte=bedrooms)

    properties_data = []
    for prop in queryset:
        clean_price = 0
        try:
            clean_price = float(re.sub(r'[^\d.]', '', prop.property_budget))
        except:
            clean_price = 0

        if min_price and min_price.isdigit() and clean_price < float(min_price):
            continue
        if max_price and max_price.isdigit() and clean_price > float(max_price):
            continue

        reviews = property_review.objects.filter(property_id=prop.id)
        avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 5.0
        review_count = reviews.count()

        properties_data.append({
            'prop': prop,
            'avg_rating': round(avg_rating, 1),
            'review_count': review_count,
            'reviews': reviews.order_by('-created_at')[:3]
        })

    wishlist_items = []
    user_bookings = {}
    if request.session.get('uid'):
        user_id = str(request.session['uid'])
        wishlist_items = list(wishlists.objects.filter(user_id=user_id).values_list('property_name', flat=True))
        user_bookings = {b.property_id: b for b in property_booking.objects.filter(user_id=user_id)}

    for item in properties_data:
        item['prop'].user_booking = user_bookings.get(item['prop'].id)

    return render(request, 'myprop.html', {
        'properties_data': properties_data,
        'builder_properties': [item['prop'] for item in properties_data],
        'wishlist_items': wishlist_items,
        'selected_category': category,
        'selected_keyword': keyword,
        'selected_min_price': min_price,
        'selected_max_price': max_price,
        'selected_bedrooms': bedrooms
    })

def add_review(request, id):
    if not request.session.get('uid'):
        return redirect('/login')
    if request.method == 'POST':
        user_id = str(request.session['uid'])
        user_name = request.session.get('uname', 'Verified Client')
        rating = int(request.POST.get('rating', 5))
        comment = request.POST.get('comment', '').strip()
        if comment:
            property_review.objects.create(
                user_id=user_id,
                user_name=user_name,
                property_id=id,
                rating=rating,
                comment=comment
            )
    return redirect('/viewprop')

# -------------------------------------------------------------
# 2. AVAILABILITY CALENDAR & VISIT TIME SLOTS
# -------------------------------------------------------------
STANDARD_TIME_SLOTS = [
    '10:00 AM - 11:00 AM',
    '11:00 AM - 12:00 PM',
    '02:00 PM - 03:00 PM',
    '04:00 PM - 05:00 PM'
]

def check_availability(request, id):
    prop = get_object_or_404(property_details, pk=id)
    selected_date_str = request.GET.get('date', str(date.today()))
    
    try:
        selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
    except ValueError:
        selected_date = date.today()

    # Query booked slots for this property on selected date
    booked_visits = property_visit.objects.filter(
        property_id=id,
        visit_date=selected_date,
        status__in=['Pending', 'Confirmed']
    ).values_list('time_slot', flat=True)

    slots_status = []
    for slot in STANDARD_TIME_SLOTS:
        slots_status.append({
            'slot': slot,
            'is_booked': slot in booked_visits
        })

    # Fetch builder info
    builder = approved_builder_details.objects.filter(pk=prop.user_id).first()

    return render(request, 'availability_calendar.html', {
        'prop': prop,
        'selected_date': str(selected_date),
        'today_date': str(date.today()),
        'slots_status': slots_status,
        'builder': builder
    })

def schedulevisit_slot(request, id):
    if not request.session.get('uid'):
        return redirect('/login')
    
    user_id = str(request.session['uid'])
    udata = user_details.objects.filter(pk=user_id).first()
    pdata = get_object_or_404(property_details, pk=id)

    if request.method == 'POST':
        visit_date_str = request.POST.get('visit_date', str(date.today()))
        time_slot = request.POST.get('time_slot', '').strip()

        try:
            visit_date = datetime.strptime(visit_date_str, '%Y-%m-%d').date()
        except ValueError:
            visit_date = date.today()

        # Prevent duplicate/conflicting slot bookings
        existing_conflict = property_visit.objects.filter(
            property_id=id,
            visit_date=visit_date,
            time_slot=time_slot,
            status__in=['Pending', 'Confirmed']
        ).exists()

        if existing_conflict:
            return render(request, 'availability_calendar.html', {
                'prop': pdata,
                'selected_date': str(visit_date),
                'today_date': str(date.today()),
                'error': f'The slot "{time_slot}" on {visit_date} is already booked! Please select another slot.',
                'slots_status': [{'slot': s, 'is_booked': True if s == time_slot else False} for s in STANDARD_TIME_SLOTS]
            })

        # Save visit
        vdata = property_visit.objects.create(
            user_id=user_id,
            user_name=udata.name if udata else 'Client',
            user_email=udata.email if udata else '',
            user_phone=udata.phone if udata else '',
            builder_id=pdata.user_id,
            property_id=id,
            property_name=pdata.property_name,
            property_location=pdata.property_location,
            property_budget=pdata.property_budget,
            visit_date=visit_date,
            time_slot=time_slot,
            status='Pending'
        )

        # Legacy booking entry for backwards compatibility
        booking.objects.create(
            user_id=user_id,
            name=udata.name if udata else 'Client',
            email=udata.email if udata else '',
            phone=udata.phone if udata else '',
            property_name=pdata.property_name,
            property_location=pdata.property_location,
            property_budget=pdata.property_budget
        )

        # Send Builder Notification
        send_notification(
            recipient_type='builder',
            recipient_id=pdata.user_id,
            title='New Visit Request',
            message=f'{udata.name if udata else "A client"} requested a site visit for "{pdata.property_name}" on {visit_date} ({time_slot}).',
            link='/my_visits'
        )

        # Send Admin Notification
        send_notification(
            recipient_type='admin',
            recipient_id='admin',
            title='New Site Visit Scheduled',
            message=f'Visit requested for "{pdata.property_name}" on {visit_date}.',
            link='/my_visits'
        )

        return redirect('/my_visits')

    return redirect(f'/check_availability/{id}')

def schedulevisit(request, id):
    if not request.session.get('uid'):
        return redirect('/login')
    
    user_id = str(request.session['uid'])
    udata = user_details.objects.filter(pk=user_id).first()
    pdata = get_object_or_404(property_details, pk=id)

    booking.objects.create(
        user_id=user_id,
        name=udata.name if udata else 'Client',
        email=udata.email if udata else '',
        phone=udata.phone if udata else '',
        property_name=pdata.property_name,
        property_location=pdata.property_location,
        property_budget=pdata.property_budget
    )

    property_visit.objects.create(
        user_id=user_id,
        user_name=udata.name if udata else 'Client',
        user_email=udata.email if udata else '',
        user_phone=udata.phone if udata else '',
        builder_id=pdata.user_id,
        property_id=id,
        property_name=pdata.property_name,
        property_location=pdata.property_location,
        property_budget=pdata.property_budget,
        visit_date=date.today(),
        time_slot='10:00 AM - 11:00 AM',
        status='Pending'
    )

    send_notification(
        recipient_type='builder',
        recipient_id=pdata.user_id,
        title='New Visit Request',
        message=f'{udata.name if udata else "A client"} requested a site visit for "{pdata.property_name}".',
        link='/my_visits'
    )

    return redirect('/scheduledvisit')

# -------------------------------------------------------------
# 3. VISIT RESCHEDULING & WORKFLOW MANAGEMENT
# -------------------------------------------------------------
def check_and_trigger_visit_alerts(uid):
    today = date.today()
    user_visits = property_visit.objects.filter(
        user_id=str(uid),
        visit_date__gte=today,
        status__in=['Confirmed', 'Pending']
    )

    for v in user_visits:
        days_left = (v.visit_date - today).days
        if days_left <= 2:
            time_str = v.time_slot
            if days_left == 0:
                timing_desc = "today"
            elif days_left == 1:
                timing_desc = "tomorrow"
            else:
                timing_desc = f"in {days_left} days"

            notif_title = "🔔 Upcoming Property Visit"
            notif_msg = f"Your visit to {v.property_name} is scheduled for {timing_desc} ({v.visit_date.strftime('%b %d, %Y')}) at {time_str}."

            exists = notification.objects.filter(
                recipient_type='user',
                recipient_id=str(uid),
                title=notif_title,
                message=notif_msg
            ).exists()

            if not exists:
                notification.objects.create(
                    recipient_type='user',
                    recipient_id=str(uid),
                    title=notif_title,
                    message=notif_msg,
                    link='/my_visits',
                    is_read=False
                )

def property_detail_view(request, id):
    prop = get_object_or_404(property_details, pk=id)
    reviews = property_review.objects.filter(property_id=id)
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 5.0
    review_count = reviews.count()

    if request.session.get('uid'):
        uid = str(request.session['uid'])
        check_and_trigger_visit_alerts(uid)

    return render(request, 'property_details.html', {
        'prop': prop,
        'avg_rating': round(avg_rating, 1),
        'review_count': review_count,
        'reviews': reviews.order_by('-created_at')[:5]
    })

def my_visits(request):
    if request.session.get('admin'):
        visits = list(property_visit.objects.all().order_by('-id'))
        bookings_map = {(str(b.user_id), b.property_id): b for b in property_booking.objects.all()}
        for v in visits:
            v.booking = bookings_map.get((str(v.user_id), v.property_id))
    elif request.session.get('uid'):
        user_id = str(request.session['uid'])
        check_and_trigger_visit_alerts(user_id)
        visits = list(property_visit.objects.filter(user_id=user_id).order_by('-id'))
        user_bookings = {b.property_id: b for b in property_booking.objects.filter(user_id=user_id)}
        for v in visits:
            v.booking = user_bookings.get(v.property_id)
    elif request.session.get('bid'):
        builder_id = str(request.session['bid'])
        visits = list(property_visit.objects.filter(builder_id=builder_id).order_by('-id'))
        bookings_map = {(str(b.user_id), b.property_id): b for b in property_booking.objects.filter(builder_id=builder_id)}
        for v in visits:
            v.booking = bookings_map.get((str(v.user_id), v.property_id))
    else:
        return redirect('/login')

    return render(request, 'my_visits.html', {'visits': visits})

def respond_visit(request, id, action):
    visit = get_object_or_404(property_visit, pk=id)
    
    if action == 'accept':
        visit.status = 'Confirmed'
        visit.save()
        send_notification(
            recipient_type='user',
            recipient_id=visit.user_id,
            title='Visit Request Confirmed! 🎉',
            message=f'Your visit request for "{visit.property_name}" on {visit.visit_date} ({visit.time_slot}) has been accepted by the builder!',
            link='/my_visits'
        )

    elif action == 'reject':
        visit.status = 'Rejected'
        visit.save()
        send_notification(
            recipient_type='user',
            recipient_id=visit.user_id,
            title='Visit Request Declined',
            message=f'Your visit request for "{visit.property_name}" on {visit.visit_date} was declined by the builder.',
            link='/my_visits'
        )

    elif action == 'suggest':
        suggested_time = request.POST.get('suggested_time', '').strip() or request.GET.get('suggested_time', '').strip()
        visit.status = 'Rescheduled'
        visit.suggested_time = suggested_time
        visit.save()

        # Start or get chat conversation
        builder_info = approved_builder_details.objects.filter(pk=visit.builder_id).first()
        conv, _ = chat_conversation.objects.get_or_create(
            user_id=visit.user_id,
            builder_id=visit.builder_id,
            property_id=visit.property_id,
            defaults={
                'user_name': visit.user_name,
                'builder_name': builder_info.buildname if builder_info else 'Builder',
                'property_name': visit.property_name
            }
        )

        msg_text = f"Regarding your visit to {visit.property_name}: The slot {visit.time_slot} on {visit.visit_date} is not available. Suggested time: {suggested_time if suggested_time else 'Can we schedule at a different time?'}"
        
        chat_message.objects.create(
            conversation=conv,
            sender_type='builder',
            sender_id=visit.builder_id,
            receiver_type='user',
            receiver_id=visit.user_id,
            message=msg_text
        )

        send_notification(
            recipient_type='user',
            recipient_id=visit.user_id,
            title='New Visit Time Suggested 💬',
            message=f'Builder suggested a new time for "{visit.property_name}": {msg_text}',
            link=f'/chat_detail/{conv.id}'
        )
        return redirect(f'/chat_detail/{conv.id}')

    return redirect('/my_visits')

def confirm_rescheduled_visit(request, id):
    visit = get_object_or_404(property_visit, pk=id)
    if request.method == 'POST':
        visit_date_str = request.POST.get('visit_date')
        time_slot = request.POST.get('time_slot')
        if visit_date_str and time_slot:
            try:
                visit.visit_date = datetime.strptime(visit_date_str, '%Y-%m-%d').date()
            except ValueError:
                pass
            visit.time_slot = time_slot
        visit.status = 'Confirmed'
        visit.save()

        send_notification(
            recipient_type='builder',
            recipient_id=visit.builder_id,
            title='Rescheduled Visit Confirmed! ✅',
            message=f'Visit for "{visit.property_name}" confirmed for {visit.visit_date} ({visit.time_slot}).',
            link='/my_visits'
        )
        send_notification(
            recipient_type='user',
            recipient_id=visit.user_id,
            title='Visit Confirmed! ✅',
            message=f'Your visit for "{visit.property_name}" is confirmed for {visit.visit_date} ({visit.time_slot}).',
            link='/my_visits'
        )

    return redirect('/my_visits')

# -------------------------------------------------------------
# 4. PRIVATE USER–BUILDER CHAT SYSTEM
# -------------------------------------------------------------
def start_chat(request, builder_id, property_id=0):
    if not request.session.get('uid') and not request.session.get('bid'):
        return redirect('/login')

    user_id = str(request.session.get('uid', ''))
    builder_id = str(builder_id)

    if not user_id and request.session.get('bid'):
        return redirect('/chat_list')

    udata = user_details.objects.filter(pk=user_id).first()
    bdata = approved_builder_details.objects.filter(pk=builder_id).first()
    pdata = property_details.objects.filter(pk=property_id).first()

    conv, _ = chat_conversation.objects.get_or_create(
        user_id=user_id,
        builder_id=builder_id,
        property_id=property_id,
        defaults={
            'user_name': udata.name if udata else 'User',
            'builder_name': bdata.buildname if bdata else 'Builder',
            'property_name': pdata.property_name if pdata else ''
        }
    )
    return redirect(f'/chat_detail/{conv.id}')

def chat_list(request):
    if request.session.get('uid'):
        current_id = str(request.session['uid'])
        conversations = chat_conversation.objects.filter(user_id=current_id).order_by('-updated_at')
        role = 'user'
    elif request.session.get('bid'):
        current_id = str(request.session['bid'])
        conversations = chat_conversation.objects.filter(builder_id=current_id).order_by('-updated_at')
        role = 'builder'
    else:
        return redirect('/login')

    conv_data = []
    for conv in conversations:
        unread_count = conv.messages.filter(receiver_id=current_id, is_read=False).count()
        last_msg = conv.messages.all().order_by('-timestamp').first()
        conv_data.append({
            'conv': conv,
            'unread_count': unread_count,
            'last_msg': last_msg
        })

    return render(request, 'chat_list.html', {'conv_data': conv_data, 'role': role})

def chat_detail(request, conv_id):
    conv = get_object_or_404(chat_conversation, pk=conv_id)
    current_uid = str(request.session.get('uid', ''))
    current_bid = str(request.session.get('bid', ''))

    if current_uid:
        if conv.user_id != current_uid:
            return redirect('/chat_list')
        role = 'user'
        sender_id = current_uid
        receiver_id = conv.builder_id
    elif current_bid:
        if conv.builder_id != current_bid:
            return redirect('/chat_list')
        role = 'builder'
        sender_id = current_bid
        receiver_id = conv.user_id
    else:
        return redirect('/login')

    # Mark incoming messages as read
    conv.messages.filter(receiver_id=sender_id, is_read=False).update(is_read=True)

    messages_list = conv.messages.all().order_by('timestamp')
    return render(request, 'chat_detail.html', {
        'conv': conv,
        'messages_list': messages_list,
        'role': role,
        'sender_id': sender_id
    })

def send_chat_message(request, conv_id):
    conv = get_object_or_404(chat_conversation, pk=conv_id)
    current_uid = str(request.session.get('uid', ''))
    current_bid = str(request.session.get('bid', ''))

    if request.method == 'POST':
        msg_text = request.POST.get('message', '').strip()
        if msg_text:
            if current_uid and conv.user_id == current_uid:
                sender_type = 'user'
                sender_id = current_uid
                receiver_type = 'builder'
                receiver_id = conv.builder_id
                sender_name = request.session.get('uname', 'User')
            elif current_bid and conv.builder_id == current_bid:
                sender_type = 'builder'
                sender_id = current_bid
                receiver_type = 'user'
                receiver_id = conv.user_id
                sender_name = request.session.get('bname', 'Builder')
            else:
                return redirect('/login')

            chat_message.objects.create(
                conversation=conv,
                sender_type=sender_type,
                sender_id=sender_id,
                receiver_type=receiver_type,
                receiver_id=receiver_id,
                message=msg_text
            )

            conv.save() # Updates updated_at

            send_notification(
                recipient_type=receiver_type,
                recipient_id=receiver_id,
                title=f'New Message from {sender_name} 💬',
                message=msg_text[:100],
                link=f'/chat_detail/{conv.id}'
            )

    return redirect(f'/chat_detail/{conv_id}')

# -------------------------------------------------------------
# 5. IN-SYSTEM NOTIFICATION ENGINE
# -------------------------------------------------------------
def notifications_list(request):
    if request.session.get('uid'):
        current_id = str(request.session['uid'])
        check_and_trigger_visit_alerts(current_id)
        notifs = notification.objects.filter(recipient_type='user', recipient_id=current_id).order_by('-created_at')
    elif request.session.get('bid'):
        current_id = str(request.session['bid'])
        notifs = notification.objects.filter(recipient_type='builder', recipient_id=current_id).order_by('-created_at')
    elif request.session.get('admin'):
        notifs = notification.objects.filter(recipient_type='admin').order_by('-created_at')
    else:
        return redirect('/login')

    return render(request, 'notifications.html', {'notifs': notifs})

def mark_notification_read(request, id):
    notif = get_object_or_404(notification, pk=id)
    notif.is_read = True
    notif.save()
    if notif.link:
        return redirect(notif.link)
    return redirect('/notifications')

# -------------------------------------------------------------
# 6. PROPERTY BOOKING REQUEST & ADVANCE PAYMENT
# -------------------------------------------------------------
def request_booking(request, property_id):
    if not request.session.get('uid'):
        return redirect('/login')

    user_id = str(request.session['uid'])

    # Prevent duplicate booking request for the same property
    existing_booking = property_booking.objects.filter(user_id=user_id, property_id=property_id).first()
    if existing_booking:
        if existing_booking.advance_payment_status == 'Pending' and existing_booking.booking_status in ['Approved', 'Payment Pending']:
            return redirect(f'/pay_advance/{existing_booking.id}')
        return redirect('/my_bookings')

    udata = user_details.objects.filter(pk=user_id).first()
    pdata = get_object_or_404(property_details, pk=property_id)

    # Calculate prices
    try:
        price_val = float(re.sub(r'[^\d.]', '', pdata.property_budget))
    except:
        price_val = 500000.0

    advance_val = round(max(1000.0, price_val * 0.05), 2) # 5% token advance
    remaining_val = round(max(0.0, price_val - advance_val), 2)

    pbooking = property_booking.objects.create(
        user_id=user_id,
        user_name=udata.name if udata else 'Client',
        user_email=udata.email if udata else '',
        user_phone=udata.phone if udata else '',
        builder_id=pdata.user_id,
        property_id=property_id,
        property_name=pdata.property_name,
        property_location=pdata.property_location,
        property_price=price_val,
        advance_amount=advance_val,
        remaining_amount=remaining_val,
        booking_status='Requested',
        advance_payment_status='Pending'
    )

    send_notification(
        recipient_type='builder',
        recipient_id=pdata.user_id,
        title='New Property Booking Request 🏠',
        message=f'{udata.name if udata else "A client"} submitted a booking request for "{pdata.property_name}".',
        link='/my_bookings'
    )
    send_notification(
        recipient_type='admin',
        recipient_id='admin',
        title='New Booking Request',
        message=f'Booking request for "{pdata.property_name}".',
        link='/my_bookings'
    )

    return redirect('/my_bookings')

def my_bookings(request):
    if request.session.get('admin'):
        bookings = property_booking.objects.all().order_by('-id')
        role = 'admin'
    elif request.session.get('uid'):
        user_id = str(request.session['uid'])
        bookings = property_booking.objects.filter(user_id=user_id).order_by('-id')
        role = 'user'
    elif request.session.get('bid'):
        builder_id = str(request.session['bid'])
        bookings = property_booking.objects.filter(builder_id=builder_id).order_by('-id')
        role = 'builder'
    else:
        return redirect('/login')

    return render(request, 'my_bookings.html', {'bookings': bookings, 'role': role})

def manage_booking_request(request, booking_id, action):
    pbooking = get_object_or_404(property_booking, pk=booking_id)

    if action == 'approve':
        pbooking.booking_status = 'Approved' # Enables payment
        pbooking.save()
        send_notification(
            recipient_type='user',
            recipient_id=pbooking.user_id,
            title='Booking Request Approved! 💳',
            message=f'Your booking request for "{pbooking.property_name}" is APPROVED! Please pay the advance token amount (${pbooking.advance_amount}) to confirm.',
            link=f'/pay_advance/{pbooking.id}'
        )

    elif action == 'reject':
        pbooking.booking_status = 'Rejected'
        pbooking.save()
        send_notification(
            recipient_type='user',
            recipient_id=pbooking.user_id,
            title='Booking Request Rejected',
            message=f'Your booking request for "{pbooking.property_name}" was rejected by the builder.',
            link='/my_bookings'
        )

    return redirect('/my_bookings')

# -------------------------------------------------------------
# 7. SANDBOX TEST PAYMENT GATEWAY
# -------------------------------------------------------------
def pay_advance(request, booking_id):
    if not request.session.get('uid'):
        return redirect('/login')

    user_id = str(request.session['uid'])
    pbooking = get_object_or_404(property_booking, pk=booking_id)

    if pbooking.user_id != user_id:
        return redirect('/my_bookings')

    if pbooking.advance_payment_status == 'Successful' or pbooking.booking_status == 'Confirmed':
        return redirect('/my_bookings')

    return render(request, 'pay_advance.html', {'booking': pbooking})

def process_sandbox_payment(request, booking_id):
    if not request.session.get('uid'):
        return redirect('/login')

    user_id = str(request.session['uid'])
    pbooking = get_object_or_404(property_booking, pk=booking_id)

    if pbooking.user_id != user_id:
        return redirect('/my_bookings')

    if pbooking.advance_payment_status == 'Successful' or pbooking.booking_status == 'Confirmed':
        return redirect('/my_bookings')

    if request.method == 'POST':
        tx_id = f"SANDBOX-REF-{random.randint(100000, 999999)}"
        
        # Save payment transaction
        payment_transaction.objects.create(
            booking=pbooking,
            user_id=user_id,
            builder_id=pbooking.builder_id,
            property_name=pbooking.property_name,
            amount=pbooking.advance_amount,
            payment_status='Successful',
            transaction_id=tx_id,
            payment_method='Test Sandbox Gateway'
        )

        # Update booking
        pbooking.advance_payment_status = 'Successful'
        pbooking.booking_status = 'Confirmed'
        pbooking.remaining_amount = round(max(0.0, pbooking.property_price - pbooking.advance_amount), 2)
        pbooking.transaction_id = tx_id
        pbooking.payment_date = timezone.now()
        pbooking.save()

        # Notifications
        send_notification(
            recipient_type='user',
            recipient_id=user_id,
            title='Payment Successful & Booking Confirmed! 🎉',
            message=f'Advance payment of ${pbooking.advance_amount} for "{pbooking.property_name}" was successful (TxID: {tx_id}). Your booking is CONFIRMED!',
            link='/my_bookings'
        )
        send_notification(
            recipient_type='builder',
            recipient_id=pbooking.builder_id,
            title='Advance Payment Received! 💰',
            message=f'Received advance payment of ${pbooking.advance_amount} for "{pbooking.property_name}" from {pbooking.user_name}. Booking is confirmed.',
            link='/my_bookings'
        )

    return redirect('/my_bookings')

# -------------------------------------------------------------
# 8. WISHLIST TOGGLE
# -------------------------------------------------------------
def wishlist(request, id):
    if not request.session.get('uid'):
        return redirect('/login')
    user_id = str(request.session['uid'])
    pdata = get_object_or_404(property_details, pk=id)

    existing = wishlists.objects.filter(user_id=user_id, property_name=pdata.property_name)
    if existing.exists():
        existing.delete()
    else:
        wdata = wishlists(
            user_id=user_id,
            property_photo=pdata.property_photo,
            property_category=pdata.property_category,
            property_name=pdata.property_name,
            property_location=pdata.property_location,
            property_budget=pdata.property_budget,
            property_bedroom=pdata.property_bedroom,
            property_bathroom=pdata.property_bathroom,
            property_area=pdata.property_area,
            property_floor=pdata.property_floor,
            property_parking=pdata.property_parking
        )
        wdata.save()

    return redirect('/viewprop')

# -------------------------------------------------------------
# 9. USER FEEDBACK & ISSUE REPORTING
# -------------------------------------------------------------
def report_issue(request):
    if not request.session.get('uid'):
        return redirect('/login')

    user_id = str(request.session['uid'])
    udata = user_details.objects.filter(pk=user_id).first()
    uname = udata.name if udata else request.session.get('uname', 'Customer')
    uemail = udata.email if udata else ''

    user_queries = query.objects.filter(Q(user_id=user_id) | (Q(email=uemail) & ~Q(email=''))).order_by('-id')

    if request.method == 'POST':
        problem_type = request.POST.get('problem_type', '').strip()
        other_problem_type = request.POST.get('other_problem_type', '').strip()
        description = request.POST.get('description', '').strip()
        rating = request.POST.get('rating', '').strip()

        # Validation: Problem Type is REQUIRED
        if not problem_type:
            return render(request, 'report_issue.html', {
                'error': 'Please select a Problem Type before submitting.',
                'uname': uname,
                'uemail': uemail,
                'description': description,
                'rating': rating,
                'user_queries': user_queries
            })

        if problem_type == 'Other' and other_problem_type:
            final_problem_type = f"Other: {other_problem_type}"
        else:
            final_problem_type = problem_type

        # Save query/feedback report with user_id
        q = query.objects.create(
            user_id=user_id,
            name=uname,
            email=uemail,
            subject=final_problem_type,
            message=description,
            problem_type=final_problem_type,
            rating=rating,
            status='New'
        )

        # Send notification to admin
        send_notification(
            recipient_type='admin',
            recipient_id='admin',
            title=f'New Issue Reported: {final_problem_type}',
            message=f'User {uname} reported a {final_problem_type}.',
            link='/viewquery'
        )

        # Refresh user queries list after creation
        user_queries = query.objects.filter(Q(user_id=user_id) | (Q(email=uemail) & ~Q(email=''))).order_by('-id')

        return render(request, 'report_issue.html', {
            'success_msg': 'Thank you! Your report/feedback has been submitted successfully.',
            'uname': uname,
            'uemail': uemail,
            'user_queries': user_queries
        })

    return render(request, 'report_issue.html', {
        'uname': uname,
        'uemail': uemail,
        'user_queries': user_queries
    })

