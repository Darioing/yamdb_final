from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

ADMIN = 'admin'
USER = 'user'
MODERATOR = 'moderator'


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('У пользователя должен быть email адрес')
        user = self.model(
            email=self.normalize_email(email),
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **kwargs):
        user = self.create_user(
            email,
            password=password,
            **kwargs
        )
        user.role = ADMIN
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    """
    Определяем наш пользовательский класс User.
    """
    ROLES = [
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор')
    ]
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()
    confirmation_code = models.CharField(max_length=24)
    first_name = models.CharField(
        max_length=30,
        blank=True,
        verbose_name='Имя',
        help_text='Введите ваше Имя'
    )
    last_name = models.CharField(
        max_length=30,
        blank=True,
        verbose_name='Фамилия',
        help_text='Введите вашу Фамилию'
    )
    username = models.CharField(
        max_length=255,
        unique=True,
    )
    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name='О себе',
        help_text='Введите ваш текст'
    )
    email = models.EmailField(
        unique=True,
        verbose_name='Почта',
        help_text='Введите вашу почту')
    role = models.CharField(
        blank=True,
        choices=ROLES,
        default=USER,
        max_length=50
    )

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_user(self):
        return self.role == USER
