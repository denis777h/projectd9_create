from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import mail_managers
from .models import Appoiments
from .models import Post, Category



@receiver(post_save, sender=Appoiments)
def notify_managers_appointment(sender, instance, created, **kwargs):
    if created:
        subject = f'{instance.client_name} {instance.date.strftime("%d %m %Y")}'
    else:
        subject = f'Appointment changed for {instance.client_name} {instance.date.strftime("%d %m %Y")}'

    mail_managers(subject=subject, message=instance.message,)


@receiver(post_delete, sender=Appoiments)
def notify_managers_appointment_canceled(sender, instance, **kwargs):
    subject = f'{instance.client_name} has canceled his appointment!'
    mail_managers(
        subject=subject,
        message=f'Canceled appointment for {instance.date.strftime("%d %m %Y")}',
    )

    print(subject)
