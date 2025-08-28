from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    Конфигурация приложения для управления пользователями.

    Этот класс настраивает параметры приложения, включая имя приложения и
    тип поля для автоматического создания идентификаторов.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"
