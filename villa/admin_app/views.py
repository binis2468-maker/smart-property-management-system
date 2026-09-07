from django.shortcuts import render,redirect
from villa.models import query,builder_details,approved_builder_details
from villa.views import dashboardindex
from builder_app.models import property_details
from user_app . models import booking
# Create your views here.
def viewquery(request):
    #fetch all user details from database
    data=query.objects.all()
    #response to be sent to html page
    return render(request,'viewquery.html',{'response':data})

def reqbuilder(request):
    data=builder_details.objects.all()
    #response to be sent to html page
    return render(request,'reqbuilder.html',{'builders':data})

def Approve_builder(request, id):
    builder_data = builder_details.objects.get(pk=id)
    builder_det = approved_builder_details(
            buildphoto=builder_data.buildphoto,
            buildname=builder_data.buildname,
            buildemail=builder_data.buildemail,
            buildphone=builder_data.buildphone,
            buildpassword=builder_data.buildpassword )
    builder_det.save()
    builder_data.delete()
    return redirect(dashboardindex)


def Delete_builder(request,id):
    builder_data = builder_details.objects.get(pk=id)
    builder_data.delete()
    return redirect(reqbuilder)

def appbuilder(request):
    data=approved_builder_details.objects.all()
    #response to be sent to html page
    return render(request,'view_approved_builders.html',{'builders':data})

def Delete_approved_builder(request,id):
    builder_data = approved_builder_details.objects.get(pk=id)
    builder_data.delete()
    return redirect(appbuilder)

def viewprop(request):
    pdata=property_details.objects.all()
    return render(request,'myprop.html',{'builder_properties':pdata})

def scheduledvisit(request):
    pdata=booking.objects.all()
    return render(request,'bookedvisit.html',{'prop':pdata})