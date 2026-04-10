from celery import shared_task
from django.utils import timezone
from .models import Order

@shared_task
def delete_expired_orders_without_responses():
    expired = Order.objects.filter(
        expires_at__lte=timezone.now(),
        status='open',
        responses__isnull=True
    )
    count = expired.count()
    expired.delete()
    return f"Deleted {count} expired orders"