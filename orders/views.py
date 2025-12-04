# orders/views.py

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .models import Order, OrderItem
from .serializers import AddToCartSerializer, OrderSerializer, CartItemSerializer
from django.shortcuts import render


# -------------------------------------------------------------------
# ViewSet principal: pedidos + carrito + checkout + resumen
# -------------------------------------------------------------------
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    # -------------------------------------------------------------
    # AÑADIR PRODUCTO AL CARRITO
    # POST /api/orders/add_to_cart/
    # -------------------------------------------------------------
    @action(detail=False, methods=['post'])
    def add_to_cart(self, request):
        serializer = AddToCartSerializer(data=request.data)

        if serializer.is_valid():
            product = serializer.validated_data['product']
            quantity = serializer.validated_data['quantity']

            # Obtener o crear carrito del usuario
            order, _ = Order.objects.get_or_create(
                user=request.user,
                is_paid=False
            )

            # Crear o actualizar OrderItem
            item, created = OrderItem.objects.get_or_create(
                order=order,
                product=product
            )

            item.quantity = item.quantity + quantity if not created else quantity
            item.save()

            return Response(
                {'message': f'{item.quantity} x {product.name} añadido al carrito'},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # -------------------------------------------------------------
    # CHECKOUT (marcar como pagado)
    # POST /api/orders/<id>/checkout/
    # -------------------------------------------------------------
    @action(detail=True, methods=['post'])
    def checkout(self, request, pk=None):
        order = self.get_object()

        if order.user != request.user:
            return Response(
                {"detail": "No tienes permiso para pagar este pedido"},
                status=status.HTTP_403_FORBIDDEN
            )

        if order.is_paid:
            return Response(
                {"detail": "El pedido ya está pagado"},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.is_paid = True
        order.save()

        return Response(
            {"message": f"Pedido {order.id} pagado correctamente"},
            status=status.HTTP_200_OK
        )

    # -------------------------------------------------------------
    # RESUMEN DEL PEDIDO
    # GET /api/orders/<id>/summary/
    # -------------------------------------------------------------
    @action(detail=True, methods=['get'])
    def summary(self, request, pk=None):
        order = self.get_object()

        if order.user != request.user:
            return Response(
                {"detail": "No tienes permiso para ver este pedido"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = OrderSerializer(order)
        return Response(serializer.data)


# -------------------------------------------------------------------
# VISTA DEL CARRITO
# GET /api/orders/cart/
# -------------------------------------------------------------------
class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        order, _ = Order.objects.get_or_create(
            user=request.user,
            is_paid=False
        )
        items = order.items.all()
        serializer = CartItemSerializer(items, many=True)
        return Response(serializer.data)


# -------------------------------------------------------------------
# ACTUALIZAR CANTIDAD
# PATCH /api/orders/cart/item/<pk>/
# -------------------------------------------------------------------
class CartItemUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            order = Order.objects.get(user=request.user, is_paid=False)
            item = order.items.get(pk=pk)
        except OrderItem.DoesNotExist:
            return Response(
                {"detail": "Item no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        quantity = request.data.get("quantity")

        if quantity and int(quantity) > 0:
            item.quantity = int(quantity)
            item.save()
            return Response(
                {"message": f"{item.quantity} x {item.product.name} actualizado"},
                status=status.HTTP_200_OK
            )

        return Response(
            {"detail": "Cantidad inválida"},
            status=status.HTTP_400_BAD_REQUEST
        )


# -------------------------------------------------------------------
# ELIMINAR PRODUCTO DEL CARRITO
# DELETE /api/orders/cart/item/<pk>/delete/
# -------------------------------------------------------------------
class CartItemDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            order = Order.objects.get(user=request.user, is_paid=False)
            item = order.items.get(pk=pk)
            product_name = item.product.name
            item.delete()

            return Response(
                {"message": f"{product_name} eliminado del carrito"},
                status=status.HTTP_200_OK
            )

        except OrderItem.DoesNotExist:
            return Response(
                {"detail": "Item no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

def cart_page(request):
    return render(request,"cart.html")