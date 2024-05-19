import smtplib

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from materials.models import Subscription


@shared_task
def mailing_about_update_course(course_id):
    print("Отправка письма")
    subscriptions = Subscription.objects.filter(course=course_id, is_active=True)
    for subscription in subscriptions:
        if subscription.course.last_update < timezone.now() + timezone.timedelta(hours=4):
            try:
                send_mail(
                    subject="Обновление подписки на курс",
                    message=f"Курс {subscription.course.title} был обновлен",
                    from_email=EMAIL_HOST_USER,
                    recipient_list=[subscription.user.email],
                    fail_silently=False
                )
            except smtplib.SMTPException:
                raise smtplib.SMTPException
