from django.db import models
from apps.accounts.models import User
from apps.orders.models import Order

class OrderChatRoom(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='chat_rooms')
    participants = models.ManyToManyField(User, related_name='order_chats')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Chat for Order #{self.order.id}"

class OrderMessage(models.Model):
    room = models.ForeignKey(OrderChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

class ExecutorChatRoom(models.Model):
    name = models.CharField(max_length=100, blank=True)
    participants = models.ManyToManyField(User, related_name='executor_chats')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_executor_chats')
    created_at = models.DateTimeField(auto_now_add=True)
    blocked_users = models.ManyToManyField(User, related_name='blocked_in_rooms', blank=True)

class ExecutorMessage(models.Model):
    room = models.ForeignKey(ExecutorChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)