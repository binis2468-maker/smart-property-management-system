from django.shortcuts import render, redirect, get_object_or_404
from builder_app.models import property_details

def add_prop(request):
    if not request.session.get('bid'):
        return redirect('/login')
    user_id = request.session['bid']

    if request.method == 'POST':
        property_photo = request.FILES.get('property_photo')
        property_category = request.POST.get('property_category', '').strip()
        property_name = request.POST.get('property_name', '').strip()
        property_location = request.POST.get('property_location', '').strip()
        property_budget = request.POST.get('property_budget', '').strip()
        property_bedroom = request.POST.get('property_bedroom', '').strip()
        property_bathroom = request.POST.get('property_bathroom', '').strip()
        property_area = request.POST.get('property_area', '').strip()
        property_floor = request.POST.get('property_floor', '').strip()
        property_parking = request.POST.get('property_parking', '').strip()

        prop_det = property_details(
            user_id=str(user_id),
            property_photo=property_photo,
            property_category=property_category,
            property_name=property_name,
            property_location=property_location,
            property_budget=property_budget,
            property_bedroom=property_bedroom,
            property_bathroom=property_bathroom,
            property_area=property_area,
            property_floor=property_floor,
            property_parking=property_parking
        )
        prop_det.save()
        return redirect('/myprop')

    return render(request, 'addprop.html')

def myprop(request):
    if not request.session.get('bid'):
        return redirect('/login')
    bldrid = str(request.session['bid'])
    pdata = property_details.objects.filter(user_id=bldrid).order_by('-id')
    return render(request, 'myprop.html', {'builder_properties': pdata})

def edit_property(request, id):
    if not request.session.get('bid'):
        return redirect('/login')
    editp = get_object_or_404(property_details, pk=id)
    return render(request, 'editprop.html', {'prop': editp})

def edit_prop(request, id):
    if not request.session.get('bid'):
        return redirect('/login')
    prop = get_object_or_404(property_details, pk=id)

    if request.method == 'POST':
        if 'property_photo' in request.FILES and request.FILES['property_photo']:
            prop.property_photo = request.FILES['property_photo']

        prop.property_category = request.POST.get('property_category', prop.property_category).strip()
        prop.property_name = request.POST.get('property_name', prop.property_name).strip()
        prop.property_location = request.POST.get('property_location', prop.property_location).strip()
        prop.property_budget = request.POST.get('property_budget', prop.property_budget).strip()
        prop.property_bedroom = request.POST.get('property_bedroom', prop.property_bedroom).strip()
        prop.property_bathroom = request.POST.get('property_bathroom', prop.property_bathroom).strip()
        prop.property_area = request.POST.get('property_area', prop.property_area).strip()
        prop.property_floor = request.POST.get('property_floor', prop.property_floor).strip()
        prop.property_parking = request.POST.get('property_parking', prop.property_parking).strip()
        prop.save()

    return redirect('/myprop')

def delete_property(request, id):
    if not request.session.get('bid') and not request.session.get('admin'):
        return redirect('/login')
    pdata = property_details.objects.filter(pk=id).first()
    if pdata:
        pdata.delete()
    return redirect('/myprop')


