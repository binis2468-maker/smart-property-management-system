from django.shortcuts import render,redirect
from villa.models import builder_details
from builder_app.models import property_details

# Create your views here.
def add_prop(request):
    build_data=builder_details.objects.all()
    user_id=request.session['bid']
    if request.method == 'POST':
        #fetch form data
        property_photo=request.FILES['property_photo']
        property_category=request.POST.get('property_category')
        property_name=request.POST.get('property_name')
        property_location=request.POST.get('property_location')
        property_budget=request.POST.get('property_budget')
        property_bedroom=request.POST.get('property_bedroom')
        property_bathroom=request.POST.get('property_bathroom')
        property_area=request.POST.get('property_area')
        property_floor=request.POST.get('property_floor')
        property_parking=request.POST.get('property_parking')
        #store in database
        prop_det=property_details(user_id=user_id,property_photo=property_photo,property_category=property_category,property_name=property_name,property_location=property_location,property_budget=property_budget,property_bedroom=property_bedroom,property_bathroom=property_bathroom,property_area=property_area,property_floor=property_floor,property_parking=property_parking)
        #save data to database
        prop_det.save()
    return render(request,'addprop.html')

def myprop(request):
    bldrid=request.session['bid']
    pdata=property_details.objects.filter(user_id=bldrid)
    return render(request,'myprop.html',{'builder_properties':pdata})

def edit_property(request,id):
    editp=property_details.objects.get(pk=id)
    return render(request,'editprop.html',{'prop':editp})

def edit_prop(request,id):
    build_data=builder_details.objects.all()
    user_id=request.session['bid']
    if request.method == 'POST':
        #fetch form data
        property_photo=request.FILES['property_photo']
        property_category=request.POST.get('property_category')
        property_name=request.POST.get('property_name')
        property_location=request.POST.get('property_location')
        property_budget=request.POST.get('property_budget')
        property_bedroom=request.POST.get('property_bedroom')
        property_bathroom=request.POST.get('property_bathroom')
        property_area=request.POST.get('property_area')
        property_floor=request.POST.get('property_floor')
        property_parking=request.POST.get('property_parking')
        #store in database
        prop_det=property_details(id=id,user_id=user_id,property_photo=property_photo,property_category=property_category,property_name=property_name,property_location=property_location,property_budget=property_budget,property_bedroom=property_bedroom,property_bathroom=property_bathroom,property_area=property_area,property_floor=property_floor,property_parking=property_parking)
        #save data to database
        prop_det.save()
    return redirect(myprop)

def delete_property(request,id):
    pdata=property_details.objects.get(pk=id)
    pdata.delete()
    return redirect(myprop)

