from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='test@ahmed.com', password='pass'):
    """create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """"Test creating a new user with an email is successfully"""
        email = "libgdxengine@gmail.com"
        password = "ahmed1998"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """tests the email of new user us normalized"""
        email = 'ahmedFathyzain@gmail.com'
        password = 'ameded'
        user = get_user_model().objects.create_user(email, password)

        self.assertEqual(user.email, email.lower())

    def test_new_user_has_valid_email(self):
        """tests creating new user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'ahmed6546')

    def test_super_user_is_created(self):
        """tests creating new super user"""
        user = get_user_model().objects.create_superuser('sdfg', 'sadf')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """test the tag string representation"""
        tag = models.TagModel.objects.create(
            user=sample_user(),
            name='Cyber Security'
        )
        self.assertEqual(str(tag), tag.name)
