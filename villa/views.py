import re
from django.shortcuts import render, redirect
from villa.models import query, user_details, builder_details, approved_builder_details
from builder_app.models import property_details
from user_app.models import booking

def validate_email_format(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(pattern, email))

def validate_phone_format(phone):
    clean_digits = re.sub(r'\D', '', phone)
    if clean_digits.startswith('91') and len(clean_digits) == 12:
        clean_digits = clean_digits[2:]
    if len(clean_digits) == 10:
        return True, f"+91 {clean_digits}"
    return False, None

def validate_password_format(password):
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one number."
    if not re.search(r'[!@#$%^&*(),.?":{}|<>\-_+=\/~\[\]]', password):
        return False, "Password must contain at least one special symbol (!@#$%^&* etc.)."
    return True, None

def home(request):
    return render(request, 'index.html')

def index(request):
    contact_success = False
    error = None

    user_id = str(request.session.get('uid', ''))
    udata = None
    if user_id:
        udata = user_details.objects.filter(pk=user_id).first()

    uname = udata.name if udata else request.session.get('uname', '')
    uemail = udata.email if udata else ''

    if request.method == 'POST':
        problem_type = request.POST.get('problem_type', '').strip()
        other_problem_type = request.POST.get('other_problem_type', '').strip()
        description = request.POST.get('description', '').strip() or request.POST.get('message', '').strip()
        rating = request.POST.get('rating', '').strip()

        # Legacy fallback if subject was passed instead of problem_type
        subject_param = request.POST.get('subject', '').strip()
        if not problem_type and subject_param:
            problem_type = subject_param

        name = uname or request.POST.get('name', '').strip() or 'Guest User'
        email = uemail or request.POST.get('email', '').strip() or 'guest@example.com'

        if not problem_type:
            error = 'Please select a Problem Type before submitting.'
        else:
            if problem_type == 'Other' and other_problem_type:
                final_problem_type = f"Other: {other_problem_type}"
            else:
                final_problem_type = problem_type

            q = query.objects.create(
                user_id=user_id if user_id else '',
                name=name,
                email=email,
                subject=final_problem_type,
                message=description,
                problem_type=final_problem_type,
                rating=rating,
                status='New'
            )

            # Send notification to admin
            from user_app.models import notification
            notification.objects.create(
                recipient_type='admin',
                recipient_id='admin',
                title=f'New Issue Reported: {final_problem_type}',
                message=f'Report from {name}: {final_problem_type}.',
                link='/viewquery'
            )

            contact_success = True

    return render(request, 'index.html', {
        'contact_success': contact_success,
        'error': error,
        'uname': uname,
        'uemail': uemail
    })

def dashboardindex(request):
    if not request.session.get('admin'):
        return redirect('/login')
    no_of_users = user_details.objects.count()
    no_of_builders = approved_builder_details.objects.count()
    pending_builder = builder_details.objects.count()
    no_of_properties = property_details.objects.count()
    no_of_bookings = booking.objects.count()
    no_of_queries = query.objects.count()
    
    data = approved_builder_details.objects.all().order_by('-id')
    rdata = builder_details.objects.all().order_by('-id')
    recent_bookings = booking.objects.all().order_by('-id')[:5]
    recent_queries = query.objects.all().order_by('-id')[:5]

    # Category counts for visual charts
    villa_count = property_details.objects.filter(property_category__icontains='villa').count()
    apartment_count = property_details.objects.filter(property_category__icontains='appartment').count() + property_details.objects.filter(property_category__icontains='apartment').count()
    penthouse_count = property_details.objects.filter(property_category__icontains='penthouse').count()
    condo_count = property_details.objects.filter(property_category__icontains='condo').count()
    other_count = max(0, no_of_properties - (villa_count + apartment_count + penthouse_count + condo_count))

    return render(request, 'adminindex.html', {
        'usercount': no_of_users,
        'buildercount': no_of_builders,
        'reqbuilder': pending_builder,
        'unitcount': no_of_properties,
        'bookingcount': no_of_bookings,
        'querycount': no_of_queries,
        'builders': data,
        'rbuilders': rdata,
        'recent_bookings': recent_bookings,
        'recent_queries': recent_queries,
        'cat_villa': villa_count,
        'cat_apt': apartment_count,
        'cat_pent': penthouse_count,
        'cat_condo': condo_count,
        'cat_other': other_count
    })

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        if not email or not password:
            return render(request, 'login.html', {'error': 'Please enter both email and password.'})

        # 1. Admin login
        if email == 'admin@gmail.com' and password == 'admin':
            request.session['email'] = email
            request.session['admin'] = 'admin'
            return redirect('/dashboardindex')

        # 2. Regular user login
        user = user_details.objects.filter(email=email, password=password).first()
        if user:
            request.session['uid'] = user.id
            request.session['uname'] = user.name
            request.session['uemail'] = user.email
            request.session['user'] = 'user'
            return redirect('/')

        # 3. Approved builder login
        builder = approved_builder_details.objects.filter(buildemail=email, buildpassword=password).first()
        if builder:
            request.session['bid'] = builder.id
            request.session['bname'] = builder.buildname
            request.session['bemail'] = builder.buildemail
            request.session['builder'] = 'builder'
            return redirect('/')

        # 4. Check if builder is still pending approval
        if builder_details.objects.filter(buildemail=email, buildpassword=password).exists():
            return render(request, 'login.html', {'error': 'Your builder account is pending admin approval. Please check back later.'})

        return render(request, 'login.html', {'error': 'Invalid email or password. Please try again.'})

    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        photo = request.FILES.get('photo')
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()

        if not name or not email or not phone or not password:
            return render(request, 'register.html', {'error': 'Please fill in all required fields.'})

        if not validate_email_format(email):
            return render(request, 'register.html', {'error': 'Please enter a valid email address (e.g. user@example.com).'})

        valid_phone, formatted_phone = validate_phone_format(phone)
        if not valid_phone:
            return render(request, 'register.html', {'error': 'Phone number must be exactly 10 digits.'})

        valid_pwd, pwd_error = validate_password_format(password)
        if not valid_pwd:
            return render(request, 'register.html', {'error': pwd_error})

        if password != confirm_password:
            return render(request, 'register.html', {'error': 'Passwords do not match.'})

        if user_details.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'This email is already registered as a user.'})

        user_det = user_details(
            photo=photo,
            name=name,
            email=email,
            phone=formatted_phone,
            password=password
        )
        user_det.save()
        return redirect('/login')

    return render(request, 'register.html')

def buildregister(request):
    if request.method == 'POST':
        buildphoto = request.FILES.get('buildphoto')
        buildname = request.POST.get('buildname', '').strip()
        buildemail = request.POST.get('buildemail', '').strip()
        buildphone = request.POST.get('buildphone', '').strip()
        buildpassword = request.POST.get('buildpassword', '').strip()
        buildconfirm_password = request.POST.get('buildconfirm_password', '').strip()

        if not buildname or not buildemail or not buildphone or not buildpassword:
            return render(request, 'builderregister.html', {'error': 'Please fill in all required fields.'})

        if not validate_email_format(buildemail):
            return render(request, 'builderregister.html', {'error': 'Please enter a valid email address (e.g. builder@example.com).'})

        valid_phone, formatted_phone = validate_phone_format(buildphone)
        if not valid_phone:
            return render(request, 'builderregister.html', {'error': 'Phone number must be exactly 10 digits.'})

        valid_pwd, pwd_error = validate_password_format(buildpassword)
        if not valid_pwd:
            return render(request, 'builderregister.html', {'error': pwd_error})

        if buildpassword != buildconfirm_password:
            return render(request, 'builderregister.html', {'error': 'Passwords do not match.'})

        if builder_details.objects.filter(buildemail=buildemail).exists() or approved_builder_details.objects.filter(buildemail=buildemail).exists():
            return render(request, 'builderregister.html', {'error': 'This email is already registered as a builder.'})

        builder_det = builder_details(
            buildphoto=buildphoto,
            buildname=buildname,
            buildemail=buildemail,
            buildphone=formatted_phone,
            buildpassword=buildpassword
        )
        builder_det.save()
        return redirect('/login')

    return render(request, 'builderregister.html')

def logout(request):
    request.session.flush()
    return redirect('/')

