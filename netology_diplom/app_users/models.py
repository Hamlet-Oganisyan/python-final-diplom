from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django_rest_passwordreset.tokens import get_token_generator
from django.utils.translation import gettext_lazy as _
from netology_diplom import settings


class UserManager(BaseUserManager):
    """
    Миксин для управления пользователями
    """
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Создание и сохранение пользователя с указанным именем пользователя,
        электронной почтой и паролем
        """
        if not email:
            raise ValueError('Укажите адрес электронной почты!')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Стандартная модель пользователей
    """
    USER_TYPE_CHOICES = (
        ('shop', 'Магазин'),
        ('buyer', 'Покупатель'),
    )
    REQUIRED_FIELDS = []
    objects = UserManager()
    USERNAME_FIELD = 'email'
    email = models.EmailField(_('email address'), unique=True)
    company = models.CharField(verbose_name='Компания', max_length=40, blank=True)
    position = models.CharField(verbose_name='Должность', max_length=40, blank=True)
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=150,
        help_text=_('Требования: не более 150 символов. Символами могут быть только буквы, цифры и @/./+/-/_.'),
        validators=[username_validator],
        error_messages={
            'unique': _("Пользователь с таким именем уже существует."),
        },
    )
    is_active = models.BooleanField(verbose_name='Пользователь активен', default=False)

    type = models.CharField(verbose_name='Тип пользователя', choices=USER_TYPE_CHOICES, max_length=5, default='buyer')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = "Список пользователей"


class Contact(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Пользователь', related_name='contact',
                             on_delete=models.CASCADE)
    city = models.CharField(max_length=50, verbose_name='Город')
    street = models.CharField(max_length=50, verbose_name='Улица')
    house = models.CharField(max_length=50, verbose_name='Дом')
    apartment = models.CharField(max_length=50, verbose_name='Квартира')
    phone = models.CharField(max_length=20, verbose_name='Телефон')

    class Meta:
        verbose_name = 'Контакты пользователя'
        verbose_name_plural = 'Контакты пользователей'

    def __str__(self):
        return f'{self.city} {self.street} {self.house} {self.apartment}'


class ConfirmEmailToken(models.Model):
    objects = None

    class Meta:
        verbose_name = 'Токен подтверждения Email'
        verbose_name_plural = 'Токены подтверждения Email'

    @staticmethod
    def generate_key():
        """ Генерация псевдослучайного кода с использованием os.urandom and binascii.hexlify """
        return get_token_generator().generate_token()

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='confirm_email_tokens', on_delete=models.CASCADE,
                             verbose_name='Пользователь, которому пренадлежит токен')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата генерации токена')

    key = models.CharField(max_length=64, db_index=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(ConfirmEmailToken, self).save(*args, **kwargs)

    def __str__(self):
        return "Токен сброса пароля для пользователя {user}".format(user=self.user)