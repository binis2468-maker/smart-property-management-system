from django.test import TestCase, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from villa.models import user_details, builder_details, approved_builder_details, query
from builder_app.models import property_details
from user_app.models import booking, wishlists
from builder_app.views import add_prop, myprop, edit_prop, delete_property
from user_app.views import viewprop, wishlist, schedulevisit
from villa.views import validate_email_format, validate_phone_format, validate_password_format
from django.core.files.uploadedfile import SimpleUploadedFile

class WhiteBoxValidationTests(TestCase):
    def test_email_validation(self):
        self.assertTrue(validate_email_format("client@villa.com"))
        self.assertTrue(validate_email_format("john.doe+realty@agency.co.in"))
        self.assertFalse(validate_email_format("invalid-email"))
        self.assertFalse(validate_email_format("@missingusername.com"))
        self.assertFalse(validate_email_format("user@.com"))

    def test_phone_validation_indian_format(self):
        valid, formatted = validate_phone_format("9876543210")
        self.assertTrue(valid)
        self.assertEqual(formatted, "+91 9876543210")

        valid, formatted = validate_phone_format("+91 9876543210")
        self.assertTrue(valid)
        self.assertEqual(formatted, "+91 9876543210")

        # Invalid lengths
        valid, _ = validate_phone_format("12345")
        self.assertFalse(valid)
        valid, _ = validate_phone_format("1234567890123")
        self.assertFalse(valid)

    def test_password_complexity_rules(self):
        # Valid: >= 6 chars, uppercase, number, symbol
        valid, _ = validate_password_format("Villa@2025")
        self.assertTrue(valid)

        # Invalid: under 6 chars
        valid, err = validate_password_format("V@1")
        self.assertFalse(valid)
        self.assertIn("at least 6 characters", err)

        # Invalid: no uppercase
        valid, err = validate_password_format("villa@2025")
        self.assertFalse(valid)
        self.assertIn("uppercase", err)

        # Invalid: no number
        valid, err = validate_password_format("Villa@pass")
        self.assertFalse(valid)
        self.assertIn("number", err)

        # Invalid: no symbol
        valid, err = validate_password_format("Villa2025")
        self.assertFalse(valid)
        self.assertIn("special symbol", err)


class WhiteBoxModelTests(TestCase):
    def setUp(self):
        self.user = user_details.objects.create(
            name="John Doe",
            email="john@example.com",
            phone="+91 9876543210",
            password="Password@123"
        )
        self.builder = approved_builder_details.objects.create(
            buildname="Apex Builders",
            buildemail="apex@example.com",
            buildphone="+91 9876543211",
            buildpassword="ApexPassword@123"
        )
        self.prop = property_details.objects.create(
            user_id=str(self.builder.id),
            property_category="Luxury Villa",
            property_name="Oceanview Villa",
            property_location="Miami, FL",
            property_budget="1500000",
            property_bedroom="4",
            property_bathroom="4",
            property_area="350m2",
            property_floor="2",
            property_parking="2 cars"
        )

    def test_user_details_creation(self):
        self.assertEqual(self.user.name, "John Doe")
        self.assertEqual(self.user.email, "john@example.com")
        self.assertEqual(self.user.phone, "+91 9876543210")

    def test_builder_details_approval_flow_models(self):
        pending = builder_details.objects.create(
            buildname="Skyline Construction",
            buildemail="skyline@example.com",
            buildphone="+91 9876543212",
            buildpassword="Secret@123"
        )
        self.assertTrue(builder_details.objects.filter(buildemail="skyline@example.com").exists())
        
        approved = approved_builder_details.objects.create(
            buildname=pending.buildname,
            buildemail=pending.buildemail,
            buildphone=pending.buildphone,
            buildpassword=pending.buildpassword
        )
        pending.delete()
        
        self.assertFalse(builder_details.objects.filter(buildemail="skyline@example.com").exists())
        self.assertTrue(approved_builder_details.objects.filter(buildemail="skyline@example.com").exists())
        self.assertEqual(approved.buildname, "Skyline Construction")

    def test_property_details_model(self):
        self.assertEqual(self.prop.property_name, "Oceanview Villa")
        self.assertEqual(self.prop.property_category, "Luxury Villa")
        self.assertEqual(self.prop.user_id, str(self.builder.id))

    def test_query_model(self):
        q = query.objects.create(
            name="Alice Smith",
            email="alice@example.com",
            subject="Pricing Question",
            message="What are the payment terms?"
        )
        self.assertEqual(q.subject, "Pricing Question")
        self.assertEqual(query.objects.count(), 1)

    def test_booking_model(self):
        b = booking.objects.create(
            user_id=str(self.user.id),
            name=self.user.name,
            email=self.user.email,
            phone=self.user.phone,
            property_name=self.prop.property_name,
            property_location=self.prop.property_location,
            property_budget=self.prop.property_budget
        )
        self.assertEqual(b.property_name, "Oceanview Villa")
        self.assertEqual(b.user_id, str(self.user.id))

    def test_wishlist_model(self):
        w = wishlists.objects.create(
            user_id=str(self.user.id),
            property_name=self.prop.property_name,
            property_category=self.prop.property_category,
            property_location=self.prop.property_location,
            property_budget=self.prop.property_budget,
            property_bedroom=self.prop.property_bedroom,
            property_bathroom=self.prop.property_bathroom,
            property_area=self.prop.property_area,
            property_floor=self.prop.property_floor,
            property_parking=self.prop.property_parking
        )
        self.assertEqual(w.user_id, str(self.user.id))
        self.assertEqual(w.property_name, "Oceanview Villa")


class WhiteBoxViewAndSessionTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = user_details.objects.create(
            name="Jane User",
            email="jane@example.com",
            phone="+91 9998887777",
            password="JanePassword@123"
        )
        self.builder = approved_builder_details.objects.create(
            buildname="Prime Builders",
            buildemail="prime@example.com",
            buildphone="+91 9112223333",
            buildpassword="PrimePassword@123"
        )
        self.prop = property_details.objects.create(
            user_id=str(self.builder.id),
            property_category="Penthouse",
            property_name="Sky High Penthouse",
            property_location="Downtown",
            property_budget="2500000",
            property_bedroom="5",
            property_bathroom="5",
            property_area="500m2",
            property_floor="40",
            property_parking="3 spots"
        )

    def _add_session(self, request, session_dict=None):
        middleware = SessionMiddleware(lambda r: None)
        middleware.process_request(request)
        if session_dict:
            for k, v in session_dict.items():
                request.session[k] = v
        request.session.save()
        return request

    def test_unauthenticated_user_access_protection(self):
        req1 = self._add_session(self.factory.get('/add_prop'))
        res1 = add_prop(req1)
        self.assertEqual(res1.status_code, 302)
        self.assertEqual(res1.url, '/login')

        req2 = self._add_session(self.factory.get(f'/wishlist/{self.prop.id}'))
        res2 = wishlist(req2, self.prop.id)
        self.assertEqual(res2.status_code, 302)
        self.assertEqual(res2.url, '/login')

        req3 = self._add_session(self.factory.get(f'/schedulevisit/{self.prop.id}'))
        res3 = schedulevisit(req3, self.prop.id)
        self.assertEqual(res3.status_code, 302)
        self.assertEqual(res3.url, '/login')

    def test_wishlist_toggle_logic(self):
        req = self._add_session(self.factory.get(f'/wishlist/{self.prop.id}'), {'uid': self.user.id})
        
        res1 = wishlist(req, self.prop.id)
        self.assertEqual(res1.status_code, 302)
        self.assertTrue(wishlists.objects.filter(user_id=str(self.user.id), property_name=self.prop.property_name).exists())

        res2 = wishlist(req, self.prop.id)
        self.assertEqual(res2.status_code, 302)
        self.assertFalse(wishlists.objects.filter(user_id=str(self.user.id), property_name=self.prop.property_name).exists())

    def test_schedule_visit_view_logic(self):
        req = self._add_session(self.factory.get(f'/schedulevisit/{self.prop.id}'), {'uid': self.user.id})
        res = schedulevisit(req, self.prop.id)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, '/scheduledvisit')
        self.assertTrue(booking.objects.filter(user_id=str(self.user.id), property_name=self.prop.property_name).exists())

    def test_property_edit_without_new_photo(self):
        image_content = b"fake-image-bytes"
        test_file = SimpleUploadedFile("test.png", image_content, content_type="image/png")
        self.prop.property_photo = test_file
        self.prop.save()

        orig_photo = self.prop.property_photo

        req = self._add_session(self.factory.post(
            f'/edit_property/edit_prop/{self.prop.id}',
            {
                'property_category': 'Luxury Penthouse',
                'property_name': 'Sky High Penthouse Updated',
                'property_location': 'Downtown Core',
                'property_budget': '2800000',
                'property_bedroom': '6',
                'property_bathroom': '6',
                'property_area': '550m2',
                'property_floor': '41',
                'property_parking': '4 spots'
            }
        ), {'bid': self.builder.id})

        res = edit_prop(req, self.prop.id)
        self.assertEqual(res.status_code, 302)

        self.prop.refresh_from_db()
        self.assertEqual(self.prop.property_name, 'Sky High Penthouse Updated')
        self.assertEqual(self.prop.property_photo, orig_photo)
