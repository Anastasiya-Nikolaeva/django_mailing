from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUserManager(BaseUserManager):
    """
    Менеджер для модели пользователя.

    Этот класс управляет созданием обычных пользователей и суперпользователей.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Создание обычного пользователя.

        Параметры:
        email (str): Электронная почта пользователя.
        password (str, optional): Пароль пользователя.
        **extra_fields: Дополнительные поля для создания пользователя.

        Возвращает:
        CustomUser: Созданный пользователь.

        Исключения:
        ValueError: Если email не указан.
        """
        if not email:
            raise ValueError("Email должен быть указан")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Создание суперпользователя.

        Параметры:
        email (str): Электронная почта суперпользователя.
        password (str, optional): Пароль суперпользователя.
        **extra_fields: Дополнительные поля для создания суперпользователя.

        Возвращает:
        CustomUser: Созданный суперпользователь.

        Исключения:
        ValueError: Если is_staff или is_superuser не установлены в True.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Суперпользователь должен иметь is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Суперпользователь должен иметь is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """Модель пользователя."""

    username = None

    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    token = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Токен"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        """Возвращает адрес электронной почты пользователя."""
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        permissions = [("can_block_user", "Can block users")]
