from rest_framework.routers import DefaultRouter
from django.urls import path

from .views import (
    OrderViewSet,
    CartView,
    CartItemUpdateView,
    CartItemDeleteView,
    OrderSummaryView,
    CheckoutView,
    cart_page,
    InvoicePDFView,
)

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='orders')

urlpatterns = [
    path('orders/cart/', CartView.as_view(), name='cart'),
    path('orders/cart/items/<int:pk>/', CartItemUpdateView.as_view(), name='cart-item-update'),
    path('orders/cart/items/<int:pk>/delete/', CartItemDeleteView.as_view(), name='cart-item-delete'),

    path('orders/<int:pk>/summary/', OrderSummaryView.as_view(), name='orders-summary'),
    path('orders/<int:pk>/checkout/', CheckoutView.as_view(), name='orders-checkout'),

    path('cart-page/', cart_page, name='cart-page'),
    path(
    "orders/<int:pk>/invoice/",
    InvoicePDFView.as_view(),
    name="order-invoice"),


]

urlpatterns += router.urls
