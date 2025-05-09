from django.test import TestCase
from django.urls import reverse
from users.models import CustomUser
from .models import Recipient

User = CustomUser


class RecipientCreateViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com", password="testpass"
        )
        self.client.login(email="testuser@example.com", password="testpass")

    def test_recipient_create_view_accessible_by_name(self):
        response = self.client.get(reverse("mailing:recipient_create"))
        self.assertEqual(response.status_code, 200)

    def test_recipient_create_view_uses_correct_template(self):
        response = self.client.get(reverse("mailing:recipient_create"))
        self.assertTemplateUsed(response, "mailing/recipient_form.html")

    def test_recipient_create_view_creates_recipient(self):
        data = {
            "full_name": "Test Recipient",
            "email": "eritreya666@gmail.com",
        }
        response = self.client.post(reverse("mailing:recipient_create"), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Recipient.objects.filter(full_name="Test Recipient").exists())


        recipient = Recipient.objects.get(full_name="Test Recipient")
        self.assertEqual(recipient.owner, self.user)

    def test_recipient_create_view_invalid_data(self):
        data = {
            "full_name": "",
            "email": "invalid-email",
        }
        response = self.client.post(reverse("mailing:recipient_create"), data)
        self.assertEqual(
            response.status_code, 200
        )

        form = response.context["form"]
        self.assertTrue(form.errors)
        self.assertIn(
            "full_name", form.errors
        )
        self.assertIn(
            "This field is required.", form.errors["full_name"]
        )
