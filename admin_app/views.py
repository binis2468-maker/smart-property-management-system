from django.shortcuts import render, redirect, get_object_or_404
from villa.models import query, builder_details, approved_builder_details
from builder_app.models import property_details
from user_app.models import booking

def viewquery(request):
    if not request.session.get('admin'):
        return redirect('/login')
    data = query.objects.all().order_by('-id')
    return render(request, 'viewquery.html', {'response': data})

def reqbuilder(request):
    if not request.session.get('admin'):
        return redirect('/login')
    data = builder_details.objects.all().order_by('-id')
    return render(request, 'reqbuilder.html', {'builders': data})

def Approve_builder(request, id):
    if not request.session.get('admin'):
        return redirect('/login')
    builder_data = builder_details.objects.filter(pk=id).first()
    if builder_data:
        builder_det = approved_builder_details(
            buildphoto=builder_data.buildphoto,
            buildname=builder_data.buildname,
            buildemail=builder_data.buildemail,
            buildphone=builder_data.buildphone,
            buildpassword=builder_data.buildpassword
        )
        builder_det.save()
        builder_data.delete()
    return redirect('/dashboardindex')

def Delete_builder(request, id):
    if not request.session.get('admin'):
        return redirect('/login')
    builder_data = builder_details.objects.filter(pk=id).first()
    if builder_data:
        builder_data.delete()
    return redirect('/reqbuilder')

def appbuilder(request):
    if not request.session.get('admin'):
        return redirect('/login')
    data = approved_builder_details.objects.all().order_by('-id')
    return render(request, 'view_approved_builders.html', {'builders': data})

def Delete_approved_builder(request, id):
    if not request.session.get('admin'):
        return redirect('/login')
    builder_data = approved_builder_details.objects.filter(pk=id).first()
    if builder_data:
        builder_data.delete()
    return redirect('/appbuilder')

def scheduledvisit(request):
    if request.session.get('admin'):
        pdata = booking.objects.all().order_by('-id')
        return render(request, 'bookedvisit.html', {'prop': pdata})
    elif request.session.get('uid'):
        user_id = str(request.session['uid'])
        pdata = booking.objects.filter(user_id=user_id).order_by('-id')
        return render(request, 'bookedvisit.html', {'prop': pdata})
    elif request.session.get('bid'):
        bldrid = str(request.session['bid'])
        builder_props = property_details.objects.filter(user_id=bldrid).values_list('property_name', flat=True)
        pdata = booking.objects.filter(property_name__in=builder_props).order_by('-id')
        return render(request, 'bookedvisit.html', {'prop': pdata})
    return redirect('/login')