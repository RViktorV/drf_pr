from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField

from learning.models import Course, Lesson

NULLABLE = {"blank": True, "null": True}


class Users(AbstractUser):
    """
    Модель пользователя, наследуемая от AbstractUser, с модифицированной системой авторизации на основе email.

    Поля:
    - email: Электронная почта, используется как уникальный идентификатор для аутентификации.
    - phone_number: Номер телефона пользователя.
    - country: Страна проживания пользователя.
    - avatar: Аватар пользователя.
    - token: Токен для дополнительных операций (например, аутентификация через сторонние сервисы).
    - city: Город проживания пользователя.

    Атрибуты:
    - USERNAME_FIELD: Используем email вместо стандартного username для авторизации.
    - REQUIRED_FIELDS: Список обязательных полей для создания пользователя.
    """

    username = None  # Убираем поле username
    email = models.EmailField(
        unique=True, verbose_name="Email", help_text="Электронная почта"
    )

    phone_number = PhoneNumberField(
        unique=True,
        verbose_name="Телефон",
        help_text="Введите номер телефона",
        **NULLABLE,
    )
    country = CountryField(
        verbose_name="Страна",
        **NULLABLE,
        help_text="Страна проживания",
    )
    avatar = models.ImageField(
        upload_to="users/avatars/",
        **NULLABLE,
        verbose_name="Аватар",
        help_text="Загрузите аватар",
    )

    token = models.CharField(max_length=100, verbose_name="Токен", **NULLABLE)
    city = models.CharField(max_length=100, verbose_name="Город", **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        """
        Возвращает строковое представление пользователя — его email.
        """
        return self.email


class Payment(models.Model):
    """
    Модель платежа, которая хранит информацию о платежах, связанных с курсами и уроками.

    Поля:
    - user: Пользователь, совершивший платеж.
    - payment_date: Дата и время, когда был совершен платеж.
    - course: Курс, за который был осуществлен платеж.
    - lesson: Урок, за который был осуществлен платеж.
    - amount: Сумма платежа.
    - payment_method: Способ оплаты (наличные или перевод на счет).

    Методы:
    - __str__: Возвращает строковое представление платежа в формате: "email пользователя - сумма (способ оплаты)".
    """

    CASH = "cash"
    BANK_TRANSFER = "bank_transfer"

    PAYMENT_METHOD_CHOICES = [
        (CASH, "Наличные"),
        (BANK_TRANSFER, "Перевод на счет"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата оплаты")
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Оплаченный курс",
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Оплаченный урок",
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Сумма оплаты"
    )
    payment_method = models.CharField(
        max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name="Способ оплаты"
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        """
        Возвращает строковое представление платежа в формате:
        'email пользователя - сумма (способ оплаты)'.
        """
        return (
            f"{self.user.email} - {self.amount} ({self.get_payment_method_display()})"
        )
