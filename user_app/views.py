from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Avg, Count
from django.db import models
import re
from builder_app.models import property_details
from villa.models import user_details
from user_app.models import booking, wishlists, property_review

def viewprop(request):
    queryset = property_details.objects.all().order_by('-id')
    
    # Filter parameters
    category = request.GET.get('category', '').strip()
    keyword = request.GET.get('keyword', '').strip()
    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()
    bedrooms = request.GET.get('bedrooms', '').strip()

    if category and category.lower() != 'all':
        queryset = queryset.filter(property_category__icontains=category)
        
    if keyword:
        queryset = queryset.filter(
            models.Q(property_name__icontains=keyword) |
            models.Q(property_location__icontains=keyword)
        )

    if bedrooms and bedrooms.isdigit():
        queryset = queryset.filter(property_bedroom__gte=bedrooms)

    properties_data = []
    for prop in queryset:
        # Parse numeric price safely for filtering
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
    if request.session.get('uid'):
        user_id = str(request.session['uid'])
        wishlist_items = list(wishlists.objects.filter(user_id=user_id).values_list('property_name', flat=True))

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

def schedulevisit(request, id):
    if not request.session.get('uid'):
        return redirect('/login')
    user_id = request.session['uid']
    udata = user_details.objects.filter(pk=user_id).first()
    pdata = get_object_or_404(property_details, pk=id)

    if udata and pdata:
        bdata = booking(
            user_id=str(user_id),
            name=udata.name,
            email=udata.email,
            phone=udata.phone,
            property_name=pdata.property_name,
            property_location=pdata.property_location,
            property_budget=pdata.property_budget
        )
        bdata.save()
    return redirect('/scheduledvisit')

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
