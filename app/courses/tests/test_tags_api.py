from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core.models import TagModel
from courses.serializers import TagSerializer

TAGS_URL = reverse('courses:tagmodel-list')


class PublicTagsApiTest(TestCase):
    """For publicly available API"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_login_required(self):
        """test that loging is required for retrieving tags"""
        response = self.client.get(TAGS_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateTagsApiTest(TestCase):
    """test the authorized tags API"""
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            'ahmed.fathy1442@gmail.com',
            'password12',
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Test retrieving tags"""
        TagModel.objects.create(user=self.user, name='AI')
        TagModel.objects.create(user=self.user, name='ML')

        response = self.client.get(TAGS_URL)

        tags = TagModel.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_tags_limited_to_user(self):
        """test that tags retrieved is for authenticated user"""
        user2 = get_user_model().objects.create_user(
            email='mail@gmail.com',
            password='oass',
        )
        TagModel.objects.create(user=user2, name='ML Engineer')
        tag = TagModel.objects.create(user=self.user, name='Another Engineer')

        response = self.client.get(TAGS_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], tag.name)

    def test_create_tag_successful(self):
        """Test creating a new tag"""
        payload = {'name': 'test tag'}
        self.client.post(TAGS_URL, payload)

        exists = Tag.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()

        self.assertTrue(exists)

    def test_creat_tag_with_invalid_name(self):
        """test creating a new tag with invalid name"""
        payload = {'name': ''}
        res = self.client.post(TAGS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
