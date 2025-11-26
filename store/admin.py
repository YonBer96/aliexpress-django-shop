from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product

# Registrar categorías
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)}  # Genera el slug automáticamente

# Registrar productos
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'category', 'created_at', 'thumbnail_preview')
    list_filter = ('category',)  # Filtrar productos por categoría
    search_fields = ('title', 'description')  # Buscar por título o descripción

    # Mostrar miniatura de la imagen
    def thumbnail_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" />', obj.image)
        return "-"
    thumbnail_preview.short_description = "Imagen"
