from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



urlpatterns = [
    # Páginas HTML
    path("login.html", TemplateView.as_view(template_name="login.html"), name="login_page"),
    path("products.html", TemplateView.as_view(template_name="products.html"), name="products_page"),
    path("cart.html", TemplateView.as_view(template_name="cart.html"), name="cart_page"),
    path("checkout.html", TemplateView.as_view(template_name="checkout.html"), name="checkout_page"),

    # Admin
    path("admin/", admin.site.urls),

    # API
    path("api/", include("products.urls")),
    path("api/", include("orders.urls")),
    path("api/", include("users.urls")),

    # Login DRF
    path("api-auth/", include('rest_framework.urls')),

    # JWT auth endpoints
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path("products/", TemplateView.as_view(template_name="products.html"), name="products_page"),

]


