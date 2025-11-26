from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from store.models import Product
from .models import Order, OrderItem
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    # Endpoint para agregar productos al carrito
    @action(detail=False, methods=['post'])
    def add_to_cart(self, request):
        user = request.user
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        if not product_id:
            return Response({"error": "product_id es requerido"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        # Obtener o crear pedido pendiente
        order, created = Order.objects.get_or_create(user=user, status='pending')

        # Obtener o crear OrderItem
        order_item, created_item = OrderItem.objects.get_or_create(order=order, product=product)
        if not created_item:
            order_item.quantity += quantity
        else:
            order_item.quantity = quantity
        order_item.save()

        return Response({"message": f"{quantity} x {product.title} agregado al carrito"})
