from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



urlpatterns = [
    # HTML pages
    path("login.html", TemplateView.as_view(template_name="login.html"), name="login"),
    path("products/", TemplateView.as_view(template_name="products.html"), name="products_page"),
    path("cart/", TemplateView.as_view(template_name="cart.html"), name="cart"),
    path("checkout.html", TemplateView.as_view(template_name="checkout.html"), name="checkout"),

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



