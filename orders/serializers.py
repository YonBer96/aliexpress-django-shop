from rest_framework import serializers
from .models import Order, OrderItem
from products.models import Product


# ------------------------------
#   SERIALIZER DE ITEMS DEL PEDIDO
# ------------------------------
class OrderItemSerializer(serializers.ModelSerializer):

    order_id = serializers.IntegerField(source="order.id", read_only=True)
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_price = serializers.DecimalField(source="product.price", max_digits=10, decimal_places=2)

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product",
            "product_name",
            "product_price",
            "quantity",
            "order_id",
        ]


# ------------------------------
#   SERIALIZER DEL PEDIDO
# ------------------------------
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = "__all__"

    def get_total_price(self, obj):
        return float(obj.total_price)


# ------------------------------
#   SERIALIZER PARA AÑADIR AL CARRITO
# ------------------------------
class AddToCartSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all()
    )
    quantity = serializers.IntegerField(min_value=1)


# ------------------------------
#   SERIALIZER DEL CARRITO (USADO EN /api/orders/cart/)
# ------------------------------
class CartItemSerializer(serializers.ModelSerializer):

    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.FloatField(source='product.price', read_only=True)
    order_id = serializers.IntegerField(source="order.id", read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            'id',
            'product',
            'product_name',
            'product_price',
            'quantity',
            'order_id'
        ]
