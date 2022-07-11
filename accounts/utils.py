from django.contrib.auth.models import BaseUserManager
from django.utils import timezone


class CustomUserManager(BaseUserManager):

    def _create_user(self, email, password, is_staff, is_superuser, username, first_name, last_name, **extra_fields):
        now = timezone.now()

        if not email:
            raise ValueError("The given email must be set")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            username=username,
            is_staff=is_staff,
            is_superuser=is_superuser,
            date_joined=now,
            **extra_fields
        )

        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, username, first_name, last_name, **extra_fields):
        return self._create_user(email, password, True, True, username, first_name, last_name, **extra_fields)

    def create_user(self, email, password, first_name, username, last_name, **extra_fields):
        return self._create_user(email, password, True, False, username, first_name, last_name, **extra_fields)
