from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email="admin@admin.ru",
            first_name="Admin",
            last_name="Administrator",
            is_superuser=True,
            is_staff=True,
            is_active=True,
        )
        user.set_password("Admin")
        user.save()

        self.stdout.write(
            self.style.SUCCESS('создан суперпользователь\n" "admin@admin.ru\n" "Admin"')
        )
