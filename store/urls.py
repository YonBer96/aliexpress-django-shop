from django.urls import path
from .views import ProductListAPIView, CategoryListAPIView

urlpatterns = [
    path('products/', ProductListAPIView.as_view(), name='products-list'),
    path('categories/', CategoryListAPIView.as_view(), name='categories-list'),
]
