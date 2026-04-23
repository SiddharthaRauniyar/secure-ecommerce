from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Create default superuser if it does not exist"

    def handle(self, *args, **kwargs):
        username = "admin"
        email = "siddhartharauniyar5@gmail.com"
        password = "admin123"

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING("Superuser already exists"))
            return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )
        self.stdout.write(self.style.SUCCESS("Superuser created successfully"))