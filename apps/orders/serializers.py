from rest_framework import serializers
from .models import Order, Response, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')

class OrderListSerializer(serializers.ModelSerializer):
    employer_name = serializers.CharField(source='employer.username', read_only=True)
    responses_count = serializers.IntegerField(source='responses.count', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Order
        fields = ('id', 'title', 'description', 'city', 'price', 'price_type',
                  'created_at', 'status', 'employer_name', 'responses_count', 'category_name')

class ResponseSerializer(serializers.ModelSerializer):
    executor_name = serializers.CharField(source='executor.username', read_only=True)
    
    class Meta:
        model = Response
        fields = ('id', 'executor', 'executor_name', 'status', 'created_at')

class OrderDetailSerializer(serializers.ModelSerializer):
    employer = serializers.StringRelatedField()
    category = CategorySerializer()
    responses = ResponseSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = '__all__'

class OrderCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('title', 'description', 'category', 'city', 'price', 'price_type', 'required_executors')