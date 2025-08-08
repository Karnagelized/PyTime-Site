
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import environ


# Load Env
env = environ.Env()


class Command(BaseCommand):
    def handle(self, *args, **options):
        __SUPERUSER_USERNAME = env('DJANGO_SUPERUSER_USERNAME')
        __SUPERUSER_EMAIL = env('DJANGO_SUPERUSER_EMAIL')
        __SUPERUSER_PASSWORD = env('DJANGO_SUPERUSER_PASSWORD')

        usermodel = get_user_model()
        superuser = usermodel.objects.filter(email=__SUPERUSER_EMAIL).first()

        if not usermodel.objects.filter(email=__SUPERUSER_EMAIL).exists():
            try:
                superuser = usermodel.objects.create_superuser(
                    username=__SUPERUSER_USERNAME,
                    email=__SUPERUSER_EMAIL,
                    password=__SUPERUSER_PASSWORD,
                )

                self.stdout.write('Superuser created successfully.')
            except Exception as e:
                self.stdout.write('Failed to create superuser. \nError: %s' % e)
        else:
            if not all(
                [superuser.is_superuser, superuser.is_staff, superuser.is_active]
            ):
                superuser.is_superuser = True
                superuser.is_staff = True
                superuser.is_active = True
                superuser.save()

                self.stdout.write('Superuser permissions updated successfully.')

        self.stdout.write('Superuser initialized successfully.')
