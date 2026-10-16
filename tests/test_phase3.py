from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import date, timedelta

from villa.models import user_details, builder_details, approved_builder_details, query
from builder_app.models import property_details
from user_app.models import property_visit, notification

class Phase3FeaturesTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        
        # User account
        self.user = user_details.objects.create(
            name='Clark Kent',
            email='clark@dailyplanet.com',
            phone='9876543210',
            password='Password123!'
        )

        # Approved Builder
        self.builder = approved_builder_details.objects.create(
            buildphoto=SimpleUploadedFile('bldr.jpg', b'image_content', content_type='image/jpeg'),
            buildname='Metropolis Builders',
            buildemail='builder@metropolis.com',
            buildphone='9876543219',
            buildpassword='Password123!'
        )

        # Sample Properties with different Classifications
        self.prop_villa = property_details.objects.create(
            user_id=str(self.builder.id),
            property_photo=SimpleUploadedFile('villa.jpg', b'img', content_type='image/jpeg'),
            property_category='Villa',
            property_name='Metropolis Grand Villa',
            property_location='Metropolis West',
            property_budget='1200000',
            property_bedroom='4',
            property_bathroom='3',
            property_area='350m2',
            property_floor='2',
            property_parking='2 Cars',
            hospital_dist='1.5 km',
            pharmacy_dist='0.5 km',
            school_dist='2.0 km',
            supermarket_dist='1.2 km',
            bank_dist='1.0 km',
            bus_stop_dist='0.4 km',
            railway_dist='3.5 km',
            airport_dist='22 km',
            main_road_dist='0.3 km'
        )

        self.prop_condo = property_details.objects.create(
            user_id=str(self.builder.id),
            property_photo=SimpleUploadedFile('condo.jpg', b'img', content_type='image/jpeg'),
            property_category='Condo',
            property_name='Skyline Heights Condo',
            property_location='Metropolis Downtown',
            property_budget='800000',
            property_bedroom='2',
            property_bathroom='2',
            property_area='180m2',
            property_floor='12th',
            property_parking='1 Spot',
            hospital_dist='2.1 km',
            pharmacy_dist='0.2 km'
        )

    def _login_user(self):
        session = self.client.session
        session['uid'] = self.user.id
        session.save()

    def _login_builder(self):
        session = self.client.session
        session['bid'] = self.builder.id
        session.save()

    # 1. PROPERTY CLASSIFICATION DISPLAY & FILTERING
    def test_property_classification_filtering(self):
        # All Types
        res_all = self.client.get('/viewprop?category=all')
        self.assertEqual(res_all.status_code, 200)
        self.assertContains(res_all, 'Metropolis Grand Villa')
        self.assertContains(res_all, 'Skyline Heights Condo')
        self.assertContains(res_all, 'Classification: Villa')
        self.assertContains(res_all, 'Classification: Condo')

        # Villa Filter
        res_villa = self.client.get('/viewprop?category=villa')
        self.assertEqual(res_villa.status_code, 200)
        self.assertContains(res_villa, 'Metropolis Grand Villa')
        self.assertNotContains(res_villa, 'Skyline Heights Condo')

        # Condo Filter
        res_condo = self.client.get('/viewprop?category=condo')
        self.assertEqual(res_condo.status_code, 200)
        self.assertContains(res_condo, 'Skyline Heights Condo')
        self.assertNotContains(res_condo, 'Metropolis Grand Villa')

    # 2. 2D FLOOR PLAN & PROPERTY DETAILS VIEW
    def test_property_details_and_floor_plan_fallback(self):
        # Property without Floor Plan -> Shows fallback message
        res_det1 = self.client.get(f'/property_details/{self.prop_condo.id}')
        self.assertEqual(res_det1.status_code, 200)
        self.assertContains(res_det1, 'Classification: Condo')
        self.assertContains(res_det1, 'Floor plan not available for this property.')
        self.assertContains(res_det1, 'Location & Nearby Facilities')
        self.assertContains(res_det1, 'Transport & Road Connectivity')

        # Upload Floor Plan as Builder
        self._login_builder()
        floor_img = SimpleUploadedFile('fp.jpg', b'floor_plan_content', content_type='image/jpeg')
        res_edit = self.client.post(f'/edit_property/edit_prop/{self.prop_villa.id}', {
            'property_category': 'Villa',
            'property_name': 'Metropolis Grand Villa',
            'property_location': 'Metropolis West',
            'property_budget': '1200000',
            'property_bedroom': '4',
            'property_bathroom': '3',
            'property_area': '350m2',
            'property_floor': '2',
            'property_parking': '2 Cars',
            'hospital_dist': '1.8 km',
            'pharmacy_dist': '0.5 km',
            'floor_plan_image': floor_img
        })
        self.assertEqual(res_edit.status_code, 302)

        self.prop_villa.refresh_from_db()
        self.assertTrue(bool(self.prop_villa.floor_plan_image))
        self.assertEqual(self.prop_villa.hospital_dist, '1.8 km')

        # View Property Details with Floor Plan uploaded
        res_det2 = self.client.get(f'/property_details/{self.prop_villa.id}')
        self.assertEqual(res_det2.status_code, 200)
        self.assertContains(res_det2, 'Interactive 2D Floor Plan & Interior Layout')
        self.assertContains(res_det2, '1.8 km') # Hospital distance

    # 3. UPCOMING VISIT ALERTS IN NOTIFICATION SYSTEM
    def test_upcoming_visit_alerts_in_notifications(self):
        self._login_user()

        # Create visit scheduled for tomorrow
        tomorrow = date.today() + timedelta(days=1)
        visit = property_visit.objects.create(
            user_id=str(self.user.id),
            user_name=self.user.name,
            user_email=self.user.email,
            user_phone=self.user.phone,
            builder_id=str(self.builder.id),
            property_id=self.prop_villa.id,
            property_name=self.prop_villa.property_name,
            property_location=self.prop_villa.property_location,
            property_budget=self.prop_villa.property_budget,
            visit_date=tomorrow,
            time_slot='11:00 AM - 12:00 PM',
            status='Confirmed'
        )

        # Open Notifications page
        res_notif = self.client.get('/notifications')
        self.assertEqual(res_notif.status_code, 200)
        self.assertContains(res_notif, 'Upcoming Property Visit')
        self.assertContains(res_notif, 'Metropolis Grand Villa')
        self.assertContains(res_notif, 'tomorrow')

        # Check duplicate prevention: re-fetching Notifications doesn't duplicate alert
        notif_count = notification.objects.filter(recipient_type='user', recipient_id=str(self.user.id), title='🔔 Upcoming Property Visit').count()
        self.assertEqual(notif_count, 1)
