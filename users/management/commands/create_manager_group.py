from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = 'Создает группу "Менеджеры" и назначает права'

    def handle(self, *args, **options):
        # Создаем группу "Менеджеры"
        group, created = Group.objects.get_or_create(name='Менеджеры')
        self.stdout.write(self.style.SUCCESS(f"Группа 'Менеджеры' {'создана' if created else 'уже существует'}."))

        permissions = [
            'can_view_messages',
            'can_edit_messages',
            'can_delete_messages',
            'can_view_recipients',
            'can_edit_recipients',
            'can_delete_recipients',
        ]

        for perm in permissions:
            try:
                permission = Permission.objects.get(codename=perm)
                group.permissions.add(permission)
            except Permission.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"Права {perm} не найдены."))

        self.stdout.write(self.style.SUCCESS(f"Права назначены группе 'Менеджеры'."))
