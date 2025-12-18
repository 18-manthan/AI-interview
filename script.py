import os
import django
from django.conf import settings
from django.contrib.auth.models import User

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "proctoring.settings")
django.setup()


def create_users():
    if not User.objects.exists():
        # Create users
        super_user = User.objects.create_superuser(username='admin', email='admin@gmail.com', password='12345678')
        super_user.is_staff = True
        super_user.is_superuser = True
        super_user.is_active = True
        super_user.save()

create_users()

