from django.contrib import admin
from .models import OrderChatRoom, OrderMessage, ExecutorChatRoom, ExecutorMessage

admin.site.register(OrderChatRoom)
admin.site.register(OrderMessage)
admin.site.register(ExecutorChatRoom)
admin.site.register(ExecutorMessage)