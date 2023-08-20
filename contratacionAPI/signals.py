from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta
from django.utils import timezone
from .models import ContratacionMain, Notification

@receiver(post_save, sender=ContratacionMain)
def check_expiration(sender, instance, **kwargs):
    today = timezone.now().date()
    one_week_later = today + timedelta(days=7)

    if instance.finish_date > today and instance.finish_date <= one_week_later:
        # print(f"NÚMERO DE PROCESO '{instance.process_num}' está a punto de caducar {instance.finish_date - timedelta(days=7)}")
        Notification.objects.create(msg=f"NÚMERO DE PROCESO '{instance.process_num}' está a punto de caducar en 10 días y date {instance.finish_date - timedelta(days=10)}" )
