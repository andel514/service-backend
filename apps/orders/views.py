from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.utils import timezone
from .models import Order, Response, Category
from .serializers import (
    OrderListSerializer, OrderDetailSerializer,
    OrderCreateUpdateSerializer, ResponseSerializer, CategorySerializer
)
from .permissions import IsEmployerOrReadOnly, IsOrderEmployer

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

class OrderListView(generics.ListAPIView):
    serializer_class = OrderListSerializer
    permission_classes = [permissions.AllowAny]
    filterset_fields = ['category__slug', 'city', 'status', 'price_type']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'price']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Order.objects.filter(status='open', expires_at__gt=timezone.now())

class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmployerOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(employer=self.request.user)

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOrderEmployer]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OrderDetailSerializer
        return OrderCreateUpdateSerializer

class EmployerOrdersView(generics.ListAPIView):
    serializer_class = OrderListSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmployerOrReadOnly]
    
    def get_queryset(self):
        return Order.objects.filter(employer=self.request.user)

class ResponseCreateView(generics.CreateAPIView):
    serializer_class = ResponseSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        order_id = self.kwargs['order_id']
        order = Order.objects.get(pk=order_id)
        serializer.save(executor=self.request.user, order=order)

class MyResponsesView(generics.ListAPIView):
    serializer_class = ResponseSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Response.objects.filter(executor=self.request.user)