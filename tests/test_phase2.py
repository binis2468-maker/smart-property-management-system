from django.test import TestCase, Client, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from datetime import date
from villa.models import user_details, approved_builder_details, query
from builder_app.models import property_details
from user_app.models import (
    booking, wishlists, property_visit,
    chat_conversation, chat_message, notification,
    property_booking, payment_transaction
)

class Phase2FeaturesTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

        # Create test User
        self.user = user_details.objects.create(
            name="Alice Smith",
            email="alice@example.com",
            phone="+91 9876543210",
            password="AlicePassword@123"
        )

        # Create test Builder
        self.builder = approved_builder_details.objects.create(
            buildname="Apex Developers",
            buildemail="apex@example.com",
            buildphone="+91 9876543211",
            buildpassword="ApexPassword@123"
        )

        # Create test Property
        self.prop = property_details.objects.create(
            user_id=str(self.builder.id),
            property_category="Luxury Villa",
            property_name="Palm Resort Villa",
            property_location="Miami Beach, FL",
            property_budget="1000000",
            property_bedroom="4",
            property_bathroom="4",
            property_area="400m2",
            property_floor="2",
            property_parking="2 cars"
        )

    def _login_user(self):
        self.client.post('/login', {'email': 'alice@example.com', 'password': 'AlicePassword@2025'})
        session = self.client.session
        session['uid'] = self.user.id
        session['uname'] = self.user.name
        session['uemail'] = self.user.email
        session['user'] = 'user'
        session.save()

    def _login_builder(self):
        self.client.post('/login', {'email': 'apex@example.com', 'password': 'ApexPassword@2025'})
        session = self.client.session
        session['bid'] = self.builder.id
        session['bname'] = self.builder.buildname
        session['bemail'] = self.builder.buildemail
        session['builder'] = 'builder'
        session.save()

    def _login_admin(self):
        session = self.client.session
        session['admin'] = 'admin'
        session['email'] = 'admin@gmail.com'
        session.save()

    # -------------------------------------------------------------
    # TEST 1: AVAILABILITY & TIME SLOTS
    # -------------------------------------------------------------
    def test_availability_calendar_view(self):
        res = self.client.get(f'/check_availability/{self.prop.id}')
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'Palm Resort Villa')
        self.assertContains(res, '10:00 AM - 11:00 AM')

    def test_slot_booking_and_double_booking_prevention(self):
        self._login_user()
        
        # 1. Book slot
        res1 = self.client.post(f'/schedulevisit_slot/{self.prop.id}', {
            'visit_date': str(date.today()),
            'time_slot': '10:00 AM - 11:00 AM'
        })
        self.assertEqual(res1.status_code, 302)
        self.assertEqual(res1.url, '/my_visits')
        
        visit = property_visit.objects.filter(property_id=self.prop.id, time_slot='10:00 AM - 11:00 AM').first()
        self.assertIsNotNone(visit)
        self.assertEqual(visit.status, 'Pending')

        # 2. Try booking same slot again (should prevent duplicate)
        res2 = self.client.post(f'/schedulevisit_slot/{self.prop.id}', {
            'visit_date': str(date.today()),
            'time_slot': '10:00 AM - 11:00 AM'
        })
        self.assertEqual(res2.status_code, 200)
        self.assertContains(res2, 'already booked')

    # -------------------------------------------------------------
    # TEST 2: VISIT RESCHEDULING & WORKFLOW
    # -------------------------------------------------------------
    def test_visit_accept_reject_reschedule(self):
        visit = property_visit.objects.create(
            user_id=str(self.user.id),
            user_name=self.user.name,
            user_email=self.user.email,
            user_phone=self.user.phone,
            builder_id=str(self.builder.id),
            property_id=self.prop.id,
            property_name=self.prop.property_name,
            property_location=self.prop.property_location,
            property_budget=self.prop.property_budget,
            visit_date=date.today(),
            time_slot='02:00 PM - 03:00 PM',
            status='Pending'
        )

        self._login_builder()

        # Accept visit
        res_accept = self.client.get(f'/respond_visit/{visit.id}/accept')
        self.assertEqual(res_accept.status_code, 302)
        visit.refresh_from_db()
        self.assertEqual(visit.status, 'Confirmed')

        # Suggest time
        res_suggest = self.client.post(f'/respond_visit/{visit.id}/suggest', {
            'suggested_time': '04:00 PM - 05:00 PM'
        })
        self.assertEqual(res_suggest.status_code, 302)
        visit.refresh_from_db()
        self.assertEqual(visit.status, 'Rescheduled')
        self.assertEqual(visit.suggested_time, '04:00 PM - 05:00 PM')

    # -------------------------------------------------------------
    # TEST 3: PRIVATE CHAT SYSTEM & ACCESS CONTROL
    # -------------------------------------------------------------
    def test_private_chat_flow(self):
        self._login_user()

        # Start chat
        res_start = self.client.get(f'/start_chat/{self.builder.id}/{self.prop.id}')
        self.assertEqual(res_start.status_code, 302)

        conv = chat_conversation.objects.filter(user_id=str(self.user.id), builder_id=str(self.builder.id)).first()
        self.assertIsNotNone(conv)

        # Send message from user
        res_send = self.client.post(f'/send_chat_message/{conv.id}', {
            'message': 'Is this property still available for visit?'
        })
        self.assertEqual(res_send.status_code, 302)

        msg = chat_message.objects.filter(conversation=conv).first()
        self.assertIsNotNone(msg)
        self.assertEqual(msg.message, 'Is this property still available for visit?')
        self.assertEqual(msg.sender_type, 'user')

        # Check unread count for builder
        self._login_builder()
        unread_count = chat_message.objects.filter(receiver_id=str(self.builder.id), is_read=False).count()
        self.assertEqual(unread_count, 1)

        # Builder views chat detail -> marks as read
        res_detail = self.client.get(f'/chat_detail/{conv.id}')
        self.assertEqual(res_detail.status_code, 200)
        self.assertContains(res_detail, 'Is this property still available for visit?')
        msg.refresh_from_db()
        self.assertTrue(msg.is_read)

    # -------------------------------------------------------------
    # TEST 4: NOTIFICATION SYSTEM
    # -------------------------------------------------------------
    def test_notification_creation_and_mark_read(self):
        notif = notification.objects.create(
            recipient_type='user',
            recipient_id=str(self.user.id),
            title='Test Alert',
            message='Your visit was confirmed.',
            link='/my_visits'
        )

        self._login_user()
        res = self.client.get('/notifications')
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'Test Alert')

        res_read = self.client.get(f'/mark_notification_read/{notif.id}')
        self.assertEqual(res_read.status_code, 302)
        notif.refresh_from_db()
        self.assertTrue(notif.is_read)

    # -------------------------------------------------------------
    # TEST 5: BOOKING REQUEST & SANDBOX ADVANCE PAYMENT
    # -------------------------------------------------------------
    def test_booking_request_and_sandbox_payment_flow(self):
        self._login_user()

        # 1. Request booking
        res_req = self.client.get(f'/request_booking/{self.prop.id}')
        self.assertEqual(res_req.status_code, 302)
        self.assertEqual(res_req.url, '/my_bookings')

        pbooking = property_booking.objects.filter(user_id=str(self.user.id), property_id=self.prop.id).first()
        self.assertIsNotNone(pbooking)
        self.assertEqual(pbooking.booking_status, 'Requested')
        self.assertEqual(pbooking.advance_payment_status, 'Pending')
        self.assertEqual(pbooking.property_price, 1000000.0)
        self.assertEqual(pbooking.advance_amount, 50000.0) # 5% of 1,000,000

        # 2. Builder approves booking
        self._login_builder()
        res_app = self.client.get(f'/manage_booking_request/{pbooking.id}/approve')
        self.assertEqual(res_app.status_code, 302)
        pbooking.refresh_from_db()
        self.assertEqual(pbooking.booking_status, 'Approved')

        # 3. User pays advance in sandbox mode
        self._login_user()
        res_pay_page = self.client.get(f'/pay_advance/{pbooking.id}')
        self.assertEqual(res_pay_page.status_code, 200)
        self.assertContains(res_pay_page, '₹50000.0')

        res_proc = self.client.post(f'/process_sandbox_payment/{pbooking.id}')
        self.assertEqual(res_proc.status_code, 302)

        pbooking.refresh_from_db()
        self.assertEqual(pbooking.advance_payment_status, 'Successful')
        self.assertEqual(pbooking.booking_status, 'Confirmed')
        self.assertEqual(pbooking.remaining_amount, 950000.0) # 1,000,000 - 50,000

        tx = payment_transaction.objects.filter(booking=pbooking).first()
        self.assertIsNotNone(tx)
        self.assertEqual(tx.payment_status, 'Successful')
        self.assertEqual(tx.amount, 50000.0)

    # -------------------------------------------------------------
    # TEST 6: COMPLETED BOOKING STATUS IN MY VISITS & DUPLICATE PREVENTION
    # -------------------------------------------------------------
    def test_completed_booking_status_in_my_visits_and_duplicate_prevention(self):
        self._login_user()

        # 1. Create a Confirmed Visit
        visit = property_visit.objects.create(
            user_id=str(self.user.id),
            user_name=self.user.name,
            user_email=self.user.email,
            user_phone=self.user.phone,
            builder_id=str(self.builder.id),
            property_id=self.prop.id,
            property_name=self.prop.property_name,
            property_location=self.prop.property_location,
            property_budget=self.prop.property_budget,
            visit_date=date.today(),
            time_slot='10:00 AM - 11:00 AM',
            status='Confirmed'
        )

        # 2. Before booking: My Visits displays 'Request Booking'
        res_v1 = self.client.get('/my_visits')
        self.assertEqual(res_v1.status_code, 200)
        self.assertContains(res_v1, 'Request Booking')

        # 3. User requests booking
        res_req1 = self.client.get(f'/request_booking/{self.prop.id}')
        self.assertEqual(res_req1.status_code, 302)

        # Verify My Visits shows 'Booking Requested' and NOT 'Request Booking'
        res_v2 = self.client.get('/my_visits')
        self.assertEqual(res_v2.status_code, 200)
        self.assertContains(res_v2, 'Booking Requested')
        self.assertNotContains(res_v2, 'Request Booking')

        # 4. Attempting duplicate request_booking redirects and doesn't create duplicate record
        res_req2 = self.client.get(f'/request_booking/{self.prop.id}')
        self.assertEqual(res_req2.status_code, 302)
        self.assertEqual(property_booking.objects.filter(user_id=str(self.user.id), property_id=self.prop.id).count(), 1)

        # 5. Builder approves booking
        self._login_builder()
        pbooking = property_booking.objects.get(user_id=str(self.user.id), property_id=self.prop.id)
        self.client.get(f'/manage_booking_request/{pbooking.id}/approve')

        # 6. User views My Visits -> Shows 'Pay Advance', NOT 'Request Booking'
        self._login_user()
        res_v3 = self.client.get('/my_visits')
        self.assertEqual(res_v3.status_code, 200)
        self.assertContains(res_v3, 'Pay Advance')
        self.assertNotContains(res_v3, 'Request Booking')

        # 7. User processes sandbox advance payment
        res_pay = self.client.post(f'/process_sandbox_payment/{pbooking.id}')
        self.assertEqual(res_pay.status_code, 302)

        # 8. Return to My Visits -> Displays 'Booking Confirmed / Advance Paid'
        res_v4 = self.client.get('/my_visits')
        self.assertEqual(res_v4.status_code, 200)
        self.assertContains(res_v4, 'Booking Confirmed / Advance Paid')
        self.assertNotContains(res_v4, 'Request Booking')
        self.assertNotContains(res_v4, 'Pay Advance')

        # 9. Attempting duplicate payment or accessing pay_advance again redirects to /my_bookings
        res_dup_pay_page = self.client.get(f'/pay_advance/{pbooking.id}')
        self.assertEqual(res_dup_pay_page.status_code, 302)
        self.assertEqual(res_dup_pay_page.url, '/my_bookings')

        res_dup_pay_proc = self.client.post(f'/process_sandbox_payment/{pbooking.id}')
        self.assertEqual(res_dup_pay_proc.status_code, 302)
        self.assertEqual(res_dup_pay_proc.url, '/my_bookings')

    # -------------------------------------------------------------
    # TEST 7: USER FEEDBACK & ISSUE REPORTING VALIDATION & ADMIN VIEW
    # -------------------------------------------------------------
    def test_user_feedback_and_issue_reporting_validation_and_admin_view(self):
        self._login_user()

        # 1. Attempt submitting without Problem Type -> Validation Error
        res_empty = self.client.post('/report_issue', {
            'problem_type': '',
            'description': 'Test description',
            'rating': '5'
        })
        self.assertEqual(res_empty.status_code, 200)
        self.assertContains(res_empty, 'Please select a Problem Type before submitting.')
        self.assertEqual(query.objects.filter(email=self.user.email).count(), 0)

        # 2. Case 1: Submit with ONLY Problem Type -> SUCCEEDS
        res_c1 = self.client.post('/report_issue', {
            'problem_type': 'Payment Problem',
            'description': '',
            'rating': ''
        })
        self.assertEqual(res_c1.status_code, 200)
        self.assertContains(res_c1, 'Thank you! Your report/feedback has been submitted successfully.')
        q1 = query.objects.filter(email=self.user.email, problem_type='Payment Problem').first()
        self.assertIsNotNone(q1)
        self.assertEqual(q1.name, self.user.name)
        self.assertEqual(q1.message, '')

        # 3. Case 2: Submit with Problem Type + Description -> SUCCEEDS
        res_c2 = self.client.post('/report_issue', {
            'problem_type': 'Visit Problem',
            'description': 'Builder was running late for site visit',
            'rating': ''
        })
        self.assertEqual(res_c2.status_code, 200)
        q2 = query.objects.filter(email=self.user.email, problem_type='Visit Problem').first()
        self.assertIsNotNone(q2)
        self.assertEqual(q2.message, 'Builder was running late for site visit')

        # 4. Case 3: Submit with Problem Type + Rating -> SUCCEEDS
        res_c3 = self.client.post('/report_issue', {
            'problem_type': 'Website Problem',
            'description': '',
            'rating': '4'
        })
        self.assertEqual(res_c3.status_code, 200)
        q3 = query.objects.filter(email=self.user.email, problem_type='Website Problem').first()
        self.assertIsNotNone(q3)
        self.assertEqual(q3.rating, '4')

        # 5. Case 4: Submit with Problem Type + Description + Rating -> SUCCEEDS
        res_c4 = self.client.post('/report_issue', {
            'problem_type': 'Booking Problem',
            'description': 'Detailed booking issue report',
            'rating': '5'
        })
        self.assertEqual(res_c4.status_code, 200)
        q4 = query.objects.filter(email=self.user.email, problem_type='Booking Problem').first()
        self.assertIsNotNone(q4)
        self.assertEqual(q4.message, 'Detailed booking issue report')
        self.assertEqual(q4.rating, '5')

        # 6. Admin logs in and views queries/feedback
        self._login_admin()
        res_admin = self.client.get('/viewquery')
        self.assertEqual(res_admin.status_code, 200)
        self.assertContains(res_admin, self.user.name)
        self.assertContains(res_admin, self.user.email)
        self.assertContains(res_admin, 'Payment Problem')
        self.assertContains(res_admin, 'Visit Problem')
        self.assertContains(res_admin, 'No description provided')
        self.assertContains(res_admin, 'Detailed booking issue report')

    # -------------------------------------------------------------
    # TEST 8: ISSUE MARK AS READ & RESOLUTION NOTIFICATION WORKFLOW
    # -------------------------------------------------------------
    def test_issue_resolution_and_notification_workflow(self):
        # 1. Customer submits issue
        self._login_user()
        res_sub = self.client.post('/report_issue', {
            'problem_type': 'Website Problem',
            'description': 'Login page is not working properly.',
            'rating': '5'
        })
        self.assertEqual(res_sub.status_code, 200)

        q = query.objects.filter(user_id=str(self.user.id), problem_type='Website Problem').first()
        self.assertIsNotNone(q)
        self.assertEqual(q.status, 'New')

        # 2. Admin logs in and marks inquiry as Read
        self._login_admin()
        res_read = self.client.get(f'/update_query_status/{q.id}/Read')
        self.assertEqual(res_read.status_code, 302)

        q.refresh_from_db()
        self.assertEqual(q.status, 'Read')

        # Verify customer received "Admin viewed your issue" notification
        notif_read = notification.objects.filter(recipient_type='user', recipient_id=str(self.user.id), title='Admin viewed your issue').first()
        self.assertIsNotNone(notif_read)
        self.assertIn("Website Problem", notif_read.message)

        # 3. Duplicate Prevention: Repeat Mark as Read should NOT create duplicate notification
        notif_count_before = notification.objects.filter(recipient_type='user', recipient_id=str(self.user.id)).count()
        self.client.get(f'/update_query_status/{q.id}/Read')
        notif_count_after = notification.objects.filter(recipient_type='user', recipient_id=str(self.user.id)).count()
        self.assertEqual(notif_count_before, notif_count_after)

        # 4. Admin resolves inquiry with resolution details
        res_res = self.client.post(f'/update_query_status/{q.id}/Resolved', {
            'resolution_details': 'Login issue was checked and fixed.'
        })
        self.assertEqual(res_res.status_code, 302)

        q.refresh_from_db()
        self.assertEqual(q.status, 'Resolved')
        self.assertEqual(q.resolution_details, 'Login issue was checked and fixed.')
        self.assertIsNotNone(q.resolved_at)

        # Verify customer received "Your issue has been resolved" notification
        notif_res = notification.objects.filter(recipient_type='user', recipient_id=str(self.user.id), title='Your issue has been resolved').first()
        self.assertIsNotNone(notif_res)
        self.assertIn("Login issue was checked and fixed.", notif_res.message)

        # 5. Duplicate Prevention: Repeat Resolve should NOT create duplicate notification or alter resolved_at
        resolved_at_original = q.resolved_at
        notif_count_before2 = notification.objects.filter(recipient_type='user', recipient_id=str(self.user.id)).count()
        self.client.post(f'/update_query_status/{q.id}/Resolved', {
            'resolution_details': 'Attempting second resolve note.'
        })
        q.refresh_from_db()
        notif_count_after2 = notification.objects.filter(recipient_type='user', recipient_id=str(self.user.id)).count()
        self.assertEqual(notif_count_before2, notif_count_after2)
        self.assertEqual(q.resolution_details, 'Login issue was checked and fixed.')
        self.assertEqual(q.resolved_at, resolved_at_original)

        # 6. Customer logs in and views Notifications & Report Issue history
        self._login_user()
        res_notif_page = self.client.get('/notifications')
        self.assertEqual(res_notif_page.status_code, 200)
        self.assertContains(res_notif_page, 'Admin viewed your issue')
        self.assertContains(res_notif_page, 'Your issue has been resolved')

        res_rep_page = self.client.get('/report_issue')
        self.assertEqual(res_rep_page.status_code, 200)
        self.assertContains(res_rep_page, 'My Reported Issues & Feedback History')
        self.assertContains(res_rep_page, 'Login issue was checked and fixed.')

        # 7. Privacy Test: Second customer does NOT see Customer 1's notifications or issue history
        user2 = user_details.objects.create(
            name='Peter Parker',
            email='peter@parker.com',
            phone='9876543211',
            password='Password123!'
        )
        self.client.post('/login', {'email': 'peter@parker.com', 'password': 'Password123!'})

        res_u2_notif = self.client.get('/notifications')
        self.assertNotContains(res_u2_notif, 'Login issue was checked and fixed.')
        self.assertNotContains(res_u2_notif, 'Admin viewed your issue')

        res_u2_report = self.client.get('/report_issue')
        self.assertNotContains(res_u2_report, 'Login issue was checked and fixed.')

    # -------------------------------------------------------------
    # TEST 9: CUSTOMER INDEX CONTACT FORM STRUCTURED FIELDS & FIELD MAPPING
    # -------------------------------------------------------------
    def test_customer_index_contact_form_structured_fields(self):
        # Log in as Customer
        self._login_user()

        # Submit structured issue via /index Contact Us form
        res_post = self.client.post('/index', {
            'problem_type': 'Website Problem',
            'description': 'Login page is not working',
            'rating': '4'
        })
        self.assertEqual(res_post.status_code, 200)

        # Retrieve created record
        q = query.objects.filter(email=self.user.email, problem_type='Website Problem').first()
        self.assertIsNotNone(q)
        self.assertEqual(q.name, self.user.name)
        self.assertEqual(q.email, self.user.email)
        self.assertEqual(q.problem_type, 'Website Problem')
        self.assertEqual(q.message, 'Login page is not working')
        self.assertEqual(q.rating, '4')
        self.assertEqual(q.status, 'New')
        self.assertNotEqual(q.problem_type, '4')  # Ensure rating is NOT saved into problem_type

        # Admin logs in and opens Client Inquiries /viewquery
        self._login_admin()
        res_admin = self.client.get('/viewquery')
        self.assertEqual(res_admin.status_code, 200)
        self.assertContains(res_admin, self.user.name)
        self.assertContains(res_admin, self.user.email)
        self.assertContains(res_admin, 'Website Problem')
        self.assertContains(res_admin, 'Login page is not working')
        self.assertContains(res_admin, '4 / 5 Stars')
        self.assertContains(res_admin, 'New')
