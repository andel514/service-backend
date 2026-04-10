from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import OrderChatRoom, ExecutorChatRoom, ExecutorMessage
from .serializers import (
    OrderChatRoomSerializer, ExecutorChatRoomSerializer,
    OrderMessageSerializer, ExecutorMessageSerializer
)

class OrderChatRoomViewSet(viewsets.ModelViewSet):
    serializer_class = OrderChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return OrderChatRoom.objects.filter(participants=self.request.user)
    
    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        room = self.get_object()
        messages = room.messages.order_by('timestamp')
        serializer = OrderMessageSerializer(messages, many=True)
        return Response(serializer.data)

class ExecutorChatRoomViewSet(viewsets.ModelViewSet):
    serializer_class = ExecutorChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return ExecutorChatRoom.objects.filter(participants=self.request.user)
    
    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        room = self.get_object()
        messages = room.messages.filter(is_deleted=False).order_by('timestamp')
        serializer = ExecutorMessageSerializer(messages, many=True)
        return Response(serializer.data)

class ExecutorChatBlockView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, room_id):
        room = get_object_or_404(ExecutorChatRoom, id=room_id)
        if request.user in room.participants.all():
            room.blocked_users.add(request.user)
            return Response({'status': 'blocked'})
        return Response({'error': 'Not a participant'}, status=status.HTTP_403_FORBIDDEN)

class ExecutorChatUnblockView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, room_id):
        room = get_object_or_404(ExecutorChatRoom, id=room_id)
        room.blocked_users.remove(request.user)
        return Response({'status': 'unblocked'})

class ExecutorMessageDeleteView(generics.DestroyAPIView):
    queryset = ExecutorMessage.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_destroy(self, instance):
        if instance.sender == self.request.user:
            instance.is_deleted = True
            instance.save()