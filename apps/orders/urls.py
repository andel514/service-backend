from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryListView, OrderListView, OrderCreateView, OrderDetailView,
    EmployerOrdersView, ResponseCreateView, MyResponsesView
)

router = DefaultRouter()
# router.register('categories', CategoryViewSet)  # если нужно

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('', OrderListView.as_view(), name='order-list'),
    path('create/', OrderCreateView.as_view(), name='order-create'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('<int:order_id>/respond/', ResponseCreateView.as_view(), name='order-respond'),
    path('my/', EmployerOrdersView.as_view(), name='employer-orders'),
    path('responses/my/', MyResponsesView.as_view(), name='my-responses'),
]