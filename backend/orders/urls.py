from django.urls import path
from .views import (
    OrderListView,
    OrderCreateView,
    OrderDetailView,
    OrderStatusUpdateView,
    OrderCancelView
)

app_name = 'orders'

urlpatterns = [
    path('', OrderListView.as_view(), name='order-list'),
    path('create/', OrderCreateView.as_view(), name='order-create'),
    path('<int:id>/', OrderDetailView.as_view(), name='order-detail'),
    path('<int:id>/status/', OrderStatusUpdateView.as_view(), name='order-status-update'),
    path('<int:id>/cancel/', OrderCancelView.as_view(), name='order-cancel'),
]

