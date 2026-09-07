from django.shortcuts import render,redirect
from builder_app.models import property_details
from villa.models import user_details
from user_app.models import booking,wishlists
from villa.views import home,dashboardindex

# Create your views here.
def viewprop(request):
    pdata=property_details.objects.all()
    if 'uid' in request.session:
        user_id = request.session['uid']
        wishlist_items = wishlists.objects.filter(user_id=user_id).values_list('property_name')
    return render(request,'myprop.html',{'builder_properties':pdata,'wishlist_items': wishlist_items})


def schedulevisit(request,id):
    user_id=request.session['uid']
    udata=user_details.objects.get(pk=user_id)
    pdata=property_details.objects.get(pk=id)
    bdata=booking(
        user_id=user_id,
        name=udata.name,
        email=udata.email,
        phone=udata.phone,
        property_name=pdata.property_name,
        property_location=pdata.property_location,
        property_budget=pdata.property_budget
    )
    bdata.save()
    return redirect(home)

def wishlist(request,id):
    user_id=request.session['uid']
    pdata=property_details.objects.get(pk=id)
    wdata=wishlists(user_id=user_id,property_photo=pdata.property_photo,property_category=pdata.property_category,property_name=pdata.property_name,property_location=pdata.property_location,property_budget=pdata.property_budget,property_bedroom=pdata.property_bedroom,property_bathroom=pdata.property_bathroom,property_area=pdata.property_area,property_floor=pdata.property_floor,property_parking=pdata.property_parking)
        #save data to database
    wdata.save()
    return redirect(viewprop)



