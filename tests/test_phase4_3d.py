from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from villa.models import user_details, approved_builder_details
from builder_app.models import property_details

class Phase4Interactive3DViewerTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # Approved Builder
        self.builder = approved_builder_details.objects.create(
            buildphoto=SimpleUploadedFile('bldr.jpg', b'image_content', content_type='image/jpeg'),
            buildname='Royal Builders',
            buildemail='royal@builders.com',
            buildphone='9876543211',
            buildpassword='Password123!'
        )

        # Property without 3D model initially
        self.prop = property_details.objects.create(
            user_id=str(self.builder.id),
            property_photo=SimpleUploadedFile('prop.jpg', b'img', content_type='image/jpeg'),
            property_category='Villa',
            property_name='Royal Regency Villa',
            property_location='Mumbai Central',
            property_budget='15000000',
            property_bedroom='5',
            property_bathroom='4',
            property_area='450m2',
            property_floor='3',
            property_parking='3 Cars'
        )

    def _login_builder(self):
        session = self.client.session
        session['bid'] = self.builder.id
        session.save()

    def test_property_details_renders_3d_viewer_and_inr_currency(self):
        response = self.client.get(f'/property_details/{self.prop.id}')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '3D Property View')
        self.assertContains(response, 'viewer3d-container')
        self.assertContains(response, 'Drag to rotate • Scroll to zoom')
        self.assertContains(response, '₹15000000')
        self.assertNotContains(response, '$15000000')

    def test_builder_can_upload_3d_model(self):
        self._login_builder()

        model_file = SimpleUploadedFile('house.glb', b'gltf_binary_data', content_type='model/gltf-binary')
        res_edit = self.client.post(f'/edit_property/edit_prop/{self.prop.id}', {
            'property_category': 'Villa',
            'property_name': 'Royal Regency Villa',
            'property_location': 'Mumbai Central',
            'property_budget': '15000000',
            'property_bedroom': '5',
            'property_bathroom': '4',
            'property_area': '450m2',
            'property_floor': '3',
            'property_parking': '3 Cars',
            'model_3d': model_file
        })
        self.assertEqual(res_edit.status_code, 302)

        self.prop.refresh_from_db()
        self.assertTrue(bool(self.prop.model_3d))
        self.assertIn('house', self.prop.model_3d.name)

        # Details view with uploaded 3D model
        response = self.client.get(f'/property_details/{self.prop.id}')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'house')
        self.assertContains(response, 'viewer3d-container')
