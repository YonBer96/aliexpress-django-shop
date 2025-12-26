from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.shortcuts import redirect

def home_redirect(request):
    return redirect("/products.html")

urlpatterns = [
    # HTML pages
    path("login.html", TemplateView.as_view(template_name="login.html"), name="login"),
    path("products.html", TemplateView.as_view(template_name="products.html"), name="products_page"),
    path("cart.html", TemplateView.as_view(template_name="cart.html"), name="cart_page"),
    path("checkout.html", TemplateView.as_view(template_name="checkout.html"), name="checkout"),
    path("success.html", TemplateView.as_view(template_name="success.html"), name="success"),
    path("orders.html", TemplateView.as_view(template_name="orders.html"), name="orders"),
    path("order-detail.html",TemplateView.as_view(template_name="order-detail.html"),name="order_detail"),

    path("", home_redirect),
    # Admin
    path("admin/", admin.site.urls),

    # API
    path("api/", include("products.urls")),
    path("api/", include("orders.urls")),
    path("api/", include("users.urls")),

    # JWT
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]


