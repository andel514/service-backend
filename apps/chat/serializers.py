from rest_framework import serializers
from .models import OrderChatRoom, OrderMessage, ExecutorChatRoom, ExecutorMessage

class OrderMessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.username', read_only=True)
    
    class Meta:
        model = OrderMessage
        fields = ('id', 'sender', 'sender_name', 'content', 'timestamp', 'is_read')

class OrderChatRoomSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    
    class Meta:
        model = OrderChatRoom
        fields = ('id', 'order', 'created_at', 'last_message')
    
    def get_last_message(self, obj):
        last_msg = obj.messages.order_by('-timestamp').first()
        if last_msg:
            return OrderMessageSerializer(last_msg).data
        return None

class ExecutorMessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.username', read_only=True)
    
    class Meta:
        model = ExecutorMessage
        fields = ('id', 'sender', 'sender_name', 'content', 'timestamp', 'is_deleted')

class ExecutorChatRoomSerializer(serializers.ModelSerializer):
    participants = serializers.StringRelatedField(many=True)
    last_message = serializers.SerializerMethodField()
    
    class Meta:
        model = ExecutorChatRoom
        fields = ('id', 'name', 'participants', 'created_at', 'last_message')
    
    def get_last_message(self, obj):
        last_msg = obj.messages.filter(is_deleted=False).order_by('-timestamp').first()
        if last_msg:
            return ExecutorMessageSerializer(last_msg).data
        return None