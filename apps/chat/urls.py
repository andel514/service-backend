from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    OrderChatRoomViewSet, ExecutorChatRoomViewSet,
    ExecutorChatBlockView, ExecutorChatUnblockView, ExecutorMessageDeleteView
)

router = DefaultRouter()
router.register(r'order-rooms', OrderChatRoomViewSet, basename='order-chat-room')
router.register(r'executor-rooms', ExecutorChatRoomViewSet, basename='executor-chat-room')

urlpatterns = [
    path('', include(router.urls)),
    path('executor-rooms/<int:room_id>/block/', ExecutorChatBlockView.as_view(), name='executor-chat-block'),
    path('executor-rooms/<int:room_id>/unblock/', ExecutorChatUnblockView.as_view(), name='executor-chat-unblock'),
    path('executor-messages/<int:pk>/delete/', ExecutorMessageDeleteView.as_view(), name='executor-message-delete'),
]