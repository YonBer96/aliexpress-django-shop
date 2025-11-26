from django.contrib import admin
from .models import Order, OrderItem

# Registrar OrderItem por separado
admin.site.register(OrderItem)

# Inline para ver items dentro de un pedido
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

# Registro de Order con inline
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'created_at')  # quitamos total_price por ahora
    list_filter = ('status', 'created_at')
    search_fields = ('user__username',)
    inlines = [OrderItemInline]
