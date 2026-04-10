from django.urls import re_path
from apps.chat.consumers import OrderChatConsumer, ExecutorChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/order/(?P<room_id>\d+)/$', OrderChatConsumer.as_asgi()),
    re_path(r'ws/chat/executor/(?P<room_id>\d+)/$', ExecutorChatConsumer.as_asgi()),
]