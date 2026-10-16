from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from villa.models import query, builder_details, approved_builder_details, user_details
from builder_app.models import property_details
from user_app.models import booking, notification

def viewquery(request):
    if not request.session.get('admin'):
        return redirect('/login')
    data = query.objects.all().order_by('-id')
    return render(request, 'viewquery.html', {'response': data})

def update_query_status(request, id, status_val):
    if not request.session.get('admin'):
        return redirect('/login')

    q = get_object_or_404(query, pk=id)

    if status_val == 'Read':
        if q.status == 'New':
            q.status = 'Read'
            q.save()

            target_user = None
            if q.user_id:
                target_user = user_details.objects.filter(pk=q.user_id).first()
            if not target_user and q.email:
                target_user = user_details.objects.filter(email=q.email).first()

            if target_user:
                prob_type = q.problem_type or q.subject or "issue"
                notification.objects.create(
                    recipient_type='user',
                    recipient_id=str(target_user.id),
                    title="Admin viewed your issue",
                    message=f"Your submitted issue regarding '{prob_type}' has been viewed by the Admin.",
                    link="/report_issue",
                    is_read=False
                )

    elif status_val == 'Resolved':
        if q.status != 'Resolved':
            resolution_note = request.POST.get('resolution_details', '').strip() or request.GET.get('resolution_details', '').strip()
            if not resolution_note:
                resolution_note = "Issue was checked and resolved by Admin."

            q.status = 'Resolved'
            q.resolution_details = resolution_note
            q.resolved_at = timezone.now()
            q.save()

            target_user = None
            if q.user_id:
                target_user = user_details.objects.filter(pk=q.user_id).first()
            if not target_user and q.email:
                target_user = user_details.objects.filter(email=q.email).first()

            if target_user:
                prob_type = q.problem_type or q.subject or "issue"
                notification.objects.create(
                    recipient_type='user',
                    recipient_id=str(target_user.id),
                    title="Your issue has been resolved",
                    message=f"Your reported {prob_type.lower()} issue has been resolved. Resolution: {resolution_note}",
                    link="/report_issue",
                    is_read=False
                )

    return redirect('/viewquery')

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