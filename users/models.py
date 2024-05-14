from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Почта")
    phone = models.CharField(max_length=50, verbose_name="Телефон", **NULLABLE)
    city = models.CharField(max_length=100, verbose_name="Город", **NULLABLE)
    avatar = models.ImageField(
        upload_to="user_avatar/", verbose_name="Аватар", **NULLABLE
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = []

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payments(models.Model):
    CASH = "cash"
    CARD = "card"

    PAYMENT_METHOD_CHOICES = ((CASH, "Наличные"), (CARD, "Банковский перевод"))

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь", **NULLABLE
    )
    date_payment = models.DateField(auto_now=True, verbose_name="Дата оплаты")
    paid_course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name="Оплаченный курс", **NULLABLE
    )
    paid_lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, verbose_name="Оплаченный урок", **NULLABLE
    )
    payment_amount = models.PositiveIntegerField(verbose_name="Сумма оплаты")
    payment_method = models.CharField(
        max_length=50,
        choices=PAYMENT_METHOD_CHOICES,
        default=CARD,
        verbose_name="Способ оплаты",
    )

    def __str__(self):
        return f"{self.user} - {self.paid_course if self.paid_course else self.paid_lesson}"

    class Meta:
        verbose_name = "Платёж"
        verbose_name_plural = "Платежи"
        ordering = ("user", "date_payment")
