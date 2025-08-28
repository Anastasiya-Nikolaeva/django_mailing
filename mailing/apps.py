from django.apps import AppConfig


class MailingConfig(AppConfig):
    """
    Конфигурация приложения для рассылок.

    Этот класс настраивает параметры приложения, включая имя приложения и
    тип поля для автоматического создания идентификаторов.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "mailing"
