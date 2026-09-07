from django.shortcuts import render,redirect
from villa.models import query
from villa.models import user_details,builder_details,approved_builder_details
from builder_app.models import property_details

# Create your views here.

def home(request):
    return render(request,'index.html')

def dashboardindex(request):
    no_of_users=user_details.objects.count()
    no_of_builders=approved_builder_details.objects.count()
    pending_builder=builder_details.objects.count()
    data=approved_builder_details.objects.all()
    rdata=builder_details.objects.all()
    
    return render(request,'adminindex.html',{'usercount':no_of_users,'buildercount':no_of_builders,'reqbuilder':pending_builder,'builders':data,'rbuilders':rdata})


def index(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        subject=request.POST.get('subject')
        message=request.POST.get('message')
        queries=query(name=name,email=email,subject=subject,message=message)
        queries.save()
    return render(request,'index.html')


def login(request):
    email=request.POST.get('email')
    password=request.POST.get('password')
    no_of_users=user_details.objects.count()
    no_of_builders=approved_builder_details.objects.count()
    pending_builder=builder_details.objects.count()
    udata=builder_details.objects.all()
    data=approved_builder_details.objects.all()
    rdata=builder_details.objects.all()

    if email == 'admin@gmail.com' and password == 'admin':
        request.session['email']=email
        request.session['admin']='admin'
        return render(request,'adminindex.html',{'usercount':no_of_users,'buildercount':no_of_builders,'reqbuilder':pending_builder,'builders':data,'rbuilders':rdata,'udata':udata})

    elif user_details.objects.filter(email=email,password=password).exists():
        userdetails=user_details.objects.get(email=request.POST['email'],password=password)
        if userdetails.password == request.POST['password']:
            request.session['uid']=userdetails.id
            request.session['uname']=userdetails.name
            request.session['uemail']=userdetails.email
            request.session['user']='user'
            return render(request,'index.html')
    elif approved_builder_details.objects.filter(buildemail=email,buildpassword=password).exists():
        builderdetails=approved_builder_details.objects.get(buildemail=request.POST['email'],buildpassword=password)
        if builderdetails.buildpassword == request.POST['password']:
            request.session['bid']=builderdetails.id
            request.session['bname']=builderdetails.buildname
            request.session['bemail']=builderdetails.buildemail
            request.session['builder']='builder'
            return render(request,'index.html')
    return render(request,'login.html') 

def register(request):
    if request.method == 'POST':
        #fetch form data
        photo=request.FILES['photo']
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        password=request.POST.get('password')
        #store in database
        #save data to database
        if user_details.objects.filter(email=email).exists(): 
            return render(request,'register.html')
            
        else:
            User_det=user_details(photo=photo,name=name,email=email,phone=phone,password=password)
            User_det.save()
    return render(request,'register.html') 

def buildregister(request):
    if request.method == 'POST':
        buildphoto = request.FILES.get('buildphoto')
        buildname = request.POST.get('buildname')
        buildemail = request.POST.get('buildemail')
        buildphone = request.POST.get('buildphone')
        buildpassword = request.POST.get('buildpassword')

        if builder_details.objects.filter(buildemail=buildemail).exists():
            return render(request, 'builderregister.html')

        else:
            builder_det = builder_details(
                buildphoto=buildphoto,
                buildname=buildname,
                buildemail=buildemail,
                buildphone=buildphone,
                buildpassword=buildpassword
            )
            builder_det.save()

            return redirect(login)

    return render(request, 'builderregister.html')

def logout(request):
     session_key = list(request.session.keys())
     for key in session_key:
          del request.session[key]
     return redirect(index)

def viewprop(request):
    pdata=property_details.objects.all()
    return render(request,'myprop.html',{'builder_properties':pdata})
