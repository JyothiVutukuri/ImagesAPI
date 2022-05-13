import json
import tempfile

from django.contrib.auth import get_user_model
from django.contrib.sites import requests
from django.core.files import File
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import Image
from . serializers import ImageSerializer


class ImagesApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user('test@gmail.com', 'password')
        self.client.force_authenticate(self.user)

    def test_upload_images_api(self):
        upload_images_url = reverse("core:upload_images")

        invalid_csv_link = "https://www.gmail.com"
        response = self.client.post(upload_images_url, {'images_file_link': invalid_csv_link})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        valid_csv_link = "https://docs.google.com/spreadsheet/ccc?key=0Aqg9JQbnOwBwdEZFN2JKeldGZGFzUWVrNDBsczZxLUE&single=true&gid=0&output=csv"
        response = self.client.post(upload_images_url, {'images_file_link': valid_csv_link})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_api_images_list(self):
        images_list_url = reverse("core:images-list")

        Image.objects.create(title="title1", description="description2", url="www.test1image.com")
        Image.objects.create(title="title2", description="description2", url="www.test2image.com")
        response = self.client.get(images_list_url)

        images = Image.objects.all()
        serializer = ImageSerializer(images, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.data['previous'], None)
        self.assertEqual(response.data['next'], None)
        self.assertEqual(response.data['count'], 2)

    def test_retrieve_image(self):
        Image.objects.create(title="title1", description="description2", url="www.test1image.com")
        Image.objects.create(title="title2", description="description2", url="www.test2image.com")
        image_url = reverse("core:image-detail", kwargs={'pk': 1})
        response = self.client.get(image_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            "id": 1, "title": "title1", "description": "description2", "url": "www.test1image.com"
        })
