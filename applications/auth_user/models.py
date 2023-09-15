from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    """Менеджер модели CustomUser.

     Определяют email как уникальный ключ для аутентификации.
    """
    def create_user(self, email, password=None, **extra_fields):
        """Создает и сохраняет пользователя по email и password."""
        if not email:
            raise ValueError('Поле Email должно быть заполнено')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """Создает и сохраняет супер-пользователя по email и password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """Модель пользователя."""

    username = None
    password = models.CharField(
        "password",
        max_length=128,
        null=True,
        blank=True,
    )
    email = models.EmailField(unique=True)
    device = models.CharField(
        max_length=128,
        null=True,
        blank=True,
    )
    ip = models.CharField(
        max_length=128,
        null=True,
        blank=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
