from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_API = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUsersApiTest(TestCase):
    """Test Users API public"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload successful"""
        payload = {
            'email': 'ahmed.fathy144@gmail.com',
            'password': 'ahmed1998',
            'name': 'ahmed fathy',
        }
        response = self.client.post(CREATE_USER_API, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**response.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', response.data)

    def test_user_exists(self):
        """creating user that is already exists"""
        payload = {
            'email': 'ahmed.fathy1445@gmail.com',
            'password': 'ahmed1998',
        }
        create_user(**payload)

        response = self.client.post(CREATE_USER_API, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """password must be more than 5 characters"""
        payload = {
            'email': 'ahmed.fathy1445@gmail.com',
            'password': '13',
        }

        response = self.client.post(CREATE_USER_API, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        users_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(users_exists)

    def test_create_token_for_user(self):
        """test that a token is created for a user"""
        payload = {
            'email': 'ahmed.fathy1445@gmail.com',
            'password': '1234445',
        }
        create_user(**payload)

        response = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """token is not created if credentials is not valid"""

        create_user(email='ahmed.fathy1445@gmail.com', password='wrong')
        payload = {
            'email': 'ahmed.fathy1445@gmail.com',
            'password': '1234445',
        }

        response = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """test that token is not created if user doesn't exist"""
        payload = {
            'email': 'ahmed.fathy1445@gmail.com',
            'password': '1234445',
        }

        response = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_fields(self):
        """test that email and passwords are required"""
        payload = {
            'email': 'ahmed.fathy1445@gmail.com',
            'password': '',
        }
        response = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def retrieve_user_unauthorized(self):
        """test that authentication is required for users"""
        response = self.client.get(ME_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTest(TestCase):
    """Test Api that require authentication"""

    def setUp(self) -> None:
        self.user = create_user(email='test@london.com',
                                password='pass',
                                name='name')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def retrieve_profile_success(self):
        """test retrieving profile for logged in user"""
        response = self.client.get(ME_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'email': 'test@london.com',
            'name': 'name',
        })

    def test_post_not_allowed(self):
        """test that post request is not allowed in ME Url"""
        response = self.client.post(ME_URL, {})

        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """test updating profile for authenticated user"""
        payload = {
            'name': 'newName',
            'password': 'newPassword',
        }
        response = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
