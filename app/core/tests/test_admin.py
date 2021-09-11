from django.test import TestCase , Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="libgdxengine@gmail.com",
            password="ahmed1998"
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email="test@gmail.com",
            password="123",
            name="ahmed user 3ady"
        )

    def test_users_listed(self):
        """test that users are listed in users page"""
        url = reverse("admin:core_user_change_list")
        response = self.client.get(url)
        self.assertContains(response, self.user.name)
        self.assertContains(response, self.user.email)
