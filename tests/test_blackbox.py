from django.test import TestCase, Client
from villa.models import user_details, builder_details, approved_builder_details, query
from builder_app.models import property_details
from user_app.models import booking, wishlists

class BlackBoxIntegrationTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_complete_user_lifecycle(self):
        # 1. User Registration with +91 10-digit phone and complex password
        reg_resp = self.client.post('/register', {
            'name': 'Sarah Connor',
            'email': 'sarah@example.com',
            'phone': '9876543210',
            'password': 'SarahPassword@2025',
            'confirm_password': 'SarahPassword@2025'
        })
        self.assertEqual(reg_resp.status_code, 302)
        self.assertEqual(reg_resp.url, '/login')
        user = user_details.objects.filter(email='sarah@example.com').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.phone, '+91 9876543210')

        # 2. User Login
        login_resp = self.client.post('/login', {
            'email': 'sarah@example.com',
            'password': 'SarahPassword@2025'
        })
        self.assertEqual(login_resp.status_code, 302)
        self.assertEqual(login_resp.url, '/')
        self.assertIn('uid', self.client.session)

        # 3. Create property
        prop = property_details.objects.create(
            user_id='101',
            property_category='Modern Condo',
            property_name='Sunset Heights',
            property_location='San Diego, CA',
            property_budget='750000',
            property_bedroom='2',
            property_bathroom='2',
            property_area='120m2',
            property_floor='12',
            property_parking='1 spot'
        )

        # 4. View properties page
        view_resp = self.client.get('/viewprop')
        self.assertEqual(view_resp.status_code, 200)
        self.assertContains(view_resp, 'Sunset Heights')

        # 5. Wishlist property (Add)
        wl_resp1 = self.client.get(f'/wishlist/{prop.id}')
        self.assertEqual(wl_resp1.status_code, 302)
        self.assertEqual(wl_resp1.url, '/viewprop')
        self.assertEqual(wishlists.objects.filter(property_name='Sunset Heights').count(), 1)

        # 6. Schedule a visit
        visit_resp = self.client.get(f'/schedulevisit/{prop.id}')
        self.assertEqual(visit_resp.status_code, 302)
        self.assertEqual(visit_resp.url, '/scheduledvisit')
        self.assertTrue(booking.objects.filter(email='sarah@example.com', property_name='Sunset Heights').exists())

        # 7. Check scheduled visits page
        booked_page = self.client.get('/scheduledvisit')
        self.assertEqual(booked_page.status_code, 200)
        self.assertContains(booked_page, 'Sunset Heights')
        self.assertContains(booked_page, 'Sarah Connor')

        # 8. Wishlist toggle (Remove)
        wl_resp2 = self.client.get(f'/wishlist/{prop.id}')
        self.assertEqual(wl_resp2.status_code, 302)
        self.assertEqual(wishlists.objects.filter(property_name='Sunset Heights').count(), 0)

        # 9. Logout
        logout_resp = self.client.get('/logout')
        self.assertEqual(logout_resp.status_code, 302)
        self.assertNotIn('uid', self.client.session)

    def test_complete_builder_lifecycle(self):
        # 1. Builder Registration
        reg_resp = self.client.post('/buildregister', {
            'buildname': 'Horizon Homes',
            'buildemail': 'horizon@example.com',
            'buildphone': '9988776655',
            'buildpassword': 'HorizonPassword@2025',
            'buildconfirm_password': 'HorizonPassword@2025'
        })
        self.assertEqual(reg_resp.status_code, 302)
        self.assertEqual(reg_resp.url, '/login')
        builder_req = builder_details.objects.filter(buildemail='horizon@example.com').first()
        self.assertIsNotNone(builder_req)
        self.assertEqual(builder_req.buildphone, '+91 9988776655')

        # 2. Builder cannot log in before admin approval
        b_login_fail = self.client.post('/login', {
            'email': 'horizon@example.com',
            'password': 'HorizonPassword@2025'
        })
        self.assertEqual(b_login_fail.status_code, 200)
        self.assertNotIn('bid', self.client.session)

        # 3. Admin logs in and approves builder
        admin_login = self.client.post('/login', {
            'email': 'admin@gmail.com',
            'password': 'admin'
        })
        self.assertEqual(admin_login.status_code, 302)
        self.assertEqual(admin_login.url, '/dashboardindex')

        approve_resp = self.client.get(f'/Approve_builder/{builder_req.id}')
        self.assertEqual(approve_resp.status_code, 302)
        self.assertTrue(approved_builder_details.objects.filter(buildemail='horizon@example.com').exists())

        # Admin logs out
        self.client.get('/logout')

        # 4. Approved builder logs in
        b_login_success = self.client.post('/login', {
            'email': 'horizon@example.com',
            'password': 'HorizonPassword@2025'
        })
        self.assertEqual(b_login_success.status_code, 302)
        self.assertEqual(b_login_success.url, '/')
        self.assertIn('bid', self.client.session)

        # 5. Builder adds a property
        add_resp = self.client.post('/add_prop', {
            'property_category': 'Penthouse',
            'property_name': 'Horizon Skyline',
            'property_location': 'Chicago, IL',
            'property_budget': '3200000',
            'property_bedroom': '5',
            'property_bathroom': '4',
            'property_area': '400m2',
            'property_floor': '30',
            'property_parking': '2 cars'
        })
        self.assertEqual(add_resp.status_code, 302)
        self.assertEqual(add_resp.url, '/myprop')
        prop = property_details.objects.filter(property_name='Horizon Skyline').first()
        self.assertIsNotNone(prop)

        # 6. Builder views my properties
        myprop_resp = self.client.get('/myprop')
        self.assertEqual(myprop_resp.status_code, 200)
        self.assertContains(myprop_resp, 'Horizon Skyline')

        # 7. Builder edits property
        edit_resp = self.client.post(f'/edit_property/edit_prop/{prop.id}', {
            'property_category': 'Penthouse Deluxe',
            'property_name': 'Horizon Skyline Ultra',
            'property_location': 'Chicago Downtown',
            'property_budget': '3500000',
            'property_bedroom': '6',
            'property_bathroom': '5',
            'property_area': '450m2',
            'property_floor': '31',
            'property_parking': '3 cars'
        })
        self.assertEqual(edit_resp.status_code, 302)
        self.assertEqual(edit_resp.url, '/myprop')
        prop.refresh_from_db()
        self.assertEqual(prop.property_name, 'Horizon Skyline Ultra')

        # 8. Builder deletes property
        del_resp = self.client.get(f'/delete_property/{prop.id}')
        self.assertEqual(del_resp.status_code, 302)
        self.assertEqual(del_resp.url, '/myprop')
        self.assertFalse(property_details.objects.filter(id=prop.id).exists())

    def test_contact_query_submission_and_admin_view(self):
        contact_resp = self.client.post('/index', {
            'name': 'Bruce Wayne',
            'email': 'bruce@waynecorp.com',
            'subject': 'Commercial Inquiry',
            'message': 'Interested in commercial properties in Gotham.'
        })
        self.assertEqual(contact_resp.status_code, 200)
        self.assertContains(contact_resp, 'Your message has been sent successfully')
        self.assertTrue(query.objects.filter(email='bruce@waynecorp.com').exists())

        self.client.post('/login', {
            'email': 'admin@gmail.com',
            'password': 'admin'
        })
        query_page = self.client.get('/viewquery')
        self.assertEqual(query_page.status_code, 200)
        self.assertContains(query_page, 'Bruce Wayne')
        self.assertContains(query_page, 'Commercial Inquiry')
