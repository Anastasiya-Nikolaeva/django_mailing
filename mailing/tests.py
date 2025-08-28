from django.test import TestCase
from django.urls import reverse
from users.models import CustomUser
from .models import Recipient
from .services import get_index_page_cache_data
from django.core.cache import cache

User = CustomUser


class IndexViewTests(TestCase):
    def setUp(self):
        """Настройка тестового пользователя для тестов."""
        self.user = User.objects.create_user(
            email="testuser@example.com", password="testpass"
        )
        cache.clear()

    def test_index_view_accessible_by_name(self):
        """Проверка, что представление индекса доступно по имени URL для авторизованных пользователей."""
        self.client.login(email="testuser@example.com", password="testpass")
        response = self.client.get(reverse("mailing:index"))
        self.assertEqual(response.status_code, 200)

    def test_index_view_redirects_for_unauthenticated_users(self):
        """Проверка, что неавторизованные пользователи перенаправляются на страницу входа."""
        response = self.client.get(reverse("mailing:index"))
        self.assertRedirects(response, f"/user/login/?next={reverse('mailing:index')}")

    def test_index_view_context_data(self):
        """Проверка, что контекст содержит данные, возвращаемые get_index_page_cache_data."""
        self.client.login(email="testuser@example.com", password="testpass")
        response = self.client.get(reverse("mailing:index"))

        expected_data = get_index_page_cache_data(self.user)

        # Сравниваем количество элементов в QuerySet
        self.assertEqual(response.context['object_list'].count(), expected_data['object_list'].count())

        # Сравниваем остальные значения
        for key in ['attempt_count', 'attempt_success_count', 'attempt_failure_count', 'mailing_count',
                    'mailing_running_count', 'recipient_count']:
            self.assertEqual(response.context[key], expected_data[key])

class RecipientCreateViewTests(TestCase):
    def setUp(self):
        """Настройка тестового пользователя и вход в систему для тестов."""
        self.user = User.objects.create_user(
            email="testuser@example.com", password="testpass"
        )
        self.client.login(email="testuser@example.com", password="testpass")

    def test_recipient_create_view_accessible_by_name(self):
        """Проверка, что представление создания получателя доступно по его имени URL."""
        response = self.client.get(reverse("mailing:recipient_create"))
        self.assertEqual(response.status_code, 200)

    def test_recipient_create_view_uses_correct_template(self):
        """Проверка, что для представления создания получателя используется правильный шаблон."""
        response = self.client.get(reverse("mailing:recipient_create"))
        self.assertTemplateUsed(response, "mailing/recipient_form.html")

    def test_recipient_create_view_creates_recipient(self):
        """Проверка, что представление создания получателя создает нового получателя."""
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
        """Проверка, что представление создания получателя обрабатывает недействительные данные корректно."""
        data = {
            "full_name": "",
            "email": "invalid-email",
        }
        response = self.client.post(reverse("mailing:recipient_create"), data)
        self.assertEqual(response.status_code, 200)

        form = response.context["form"]
        self.assertTrue(form.errors)
        self.assertIn("full_name", form.errors)
        self.assertIn("Обязательное поле.", form.errors["full_name"])