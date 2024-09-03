from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

User = get_user_model()


class Command(BaseCommand):
    help = "create superuser from envs"

    def handle(self, *args, **kwargs):

        try:
            User.objects.create_superuser(
                username=settings.DEFAULT_SUPERUSER_NAME,
                email=settings.DEFAULT_SUPERUSER_EMAIL,
                password=settings.DEFAULT_SUPERUSER_PASSWORD,
            )
            self.stdout.write(self.style.SUCCESS(f"Superuser {settings.DEFAULT_SUPERUSER_NAME} created successfully"))
        except IntegrityError:
            self.stdout.write(
                self.style.WARNING(f"Superuser {settings.DEFAULT_SUPERUSER_NAME} already exists, skipping...")
            )
