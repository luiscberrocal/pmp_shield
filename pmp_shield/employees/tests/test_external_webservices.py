import base64

import requests
from django.test import TestCase

from django.conf import settings


class TestPhotoWebService(TestCase):
    def test_get_photo_webservice_no_photo(self):
        ip = '1795341A'
        request = requests.get(getattr(settings, 'HR_PHOTO_URL') % (ip))
        self.assertEqual(404, request.status_code)

    def test_get_photo_webservice(self):
        ip = '1795341'
        request = requests.get(getattr(settings, 'HR_PHOTO_URL') % (ip))
        if request.status_code == 200:
            with open('./output/%s.jpg' % ip, 'wb') as image_file:
                image_file.write(request.content)
            base64_image = base64.b64encode(request.content).decode('utf-8')
            self.assertTrue(base64_image.startswith('/9j/4AAQSkZJRgABAQEA5gDmAAD/4QBSRXhpZgAAS'))
        else:
            self.fail('Could not connect to web service got %d status code' % request.status_code)
