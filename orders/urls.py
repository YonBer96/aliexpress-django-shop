# orders/urls.py
# orders/urls.py

from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import (
    OrderViewSet,
    CartView,
    CartItemUpdateView,
    CartItemDeleteView,
    OrderSummaryView,
    CheckoutView
)

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='orders')

urlpatterns = [
    # Ver carrito
    path('orders/cart/', CartView.as_view(), name='cart'),

    # Actualizar cantidad
    path('orders/cart/item/<int:pk>/', CartItemUpdateView.as_view(), name='cart-item-update'),

    # Eliminar item del carrito
    path('orders/cart/item/<int:pk>/delete/', CartItemDeleteView.as_view(), name='cart-item-delete'),

    # Resumen del pedido
    path("orders/<int:pk>/summary/", OrderSummaryView.as_view(), name="orders-summary"),

    # Checkout final
    path("orders/<int:pk>/checkout/", CheckoutView.as_view(), name="orders-checkout"),
]

urlpatterns += router.urls
