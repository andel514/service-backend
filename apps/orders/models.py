from django.db import models
from django.utils import timezone
from apps.accounts.models import User

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = (
        ('open', 'Открыта'),
        ('in_progress', 'В работе'),
        ('closed', 'Закрыта'),
    )
    PRICE_TYPE_CHOICES = (
        ('hourly', 'За час'),
        ('fixed', 'Сдельная'),
    )
    
    employer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='orders')
    city = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_type = models.CharField(max_length=10, choices=PRICE_TYPE_CHOICES, default='fixed')
    required_executors = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(days=3)
        super().save(*args, **kwargs)

class Response(models.Model):
    STATUS_CHOICES = (
        ('pending', 'На рассмотрении'),
        ('accepted', 'Принят'),
        ('rejected', 'Отклонён'),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='responses')
    executor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='responses')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('order', 'executor')
    
    def __str__(self):
        return f"{self.executor.email} -> {self.order.title}"