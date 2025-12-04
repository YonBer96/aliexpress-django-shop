# orders/urls.py

from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import (
    OrderViewSet,
    CartView,
    CartItemUpdateView,
    CartItemDeleteView
)

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='orders')

urlpatterns = [
    # Ver carrito
    path('orders/cart/', CartView.as_view(), name='cart'),

    # Actualizar cantidad
    path('orders/cart/item/<int:pk>/', CartItemUpdateView.as_view(), name='cart-item-update'),

    # Eliminar item
    path('orders/cart/item/<int:pk>/delete/', CartItemDeleteView.as_view(), name='cart-item-delete'),
]

urlpatterns += router.urls

