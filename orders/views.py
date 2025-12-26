from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from datetime import datetime


from django.shortcuts import render

from .models import Order, OrderItem
from .serializers import (
    AddToCartSerializer,
    OrderSerializer,
    CartItemSerializer,
)


# ---------------------------------------------------------
# 🔥 FUNCIÓN GLOBAL PARA OBTENER O CREAR UN SOLO CARRITO ACTIVO
# ---------------------------------------------------------
def get_or_create_active_order(user):
    # Buscar todos los pedidos pendientes
    pending_orders = Order.objects.filter(
        user=user,
        is_paid=False,
        status=Order.STATUS_PENDING,
    ).order_by("id")

    if pending_orders.exists():
        order = pending_orders.first()

        # Si hay más de uno → eliminar duplicados
        if pending_orders.count() > 1:
            pending_orders.exclude(id=order.id).delete()

        return order

    # Si no hay pedido activo → crear uno
    return Order.objects.create(
        user=user,
        is_paid=False,
        status=Order.STATUS_PENDING,
    )


# ---------------------------------------------------------
#  GESTIÓN DEL PEDIDO / CARRITO
# ---------------------------------------------------------
class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    # --------------------------------------
    # Añadir productos al carrito
    # --------------------------------------
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def add_to_cart(self, request):
        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']

        # Usamos carrito activo sin duplicados
        order = get_or_create_active_order(request.user)

        item, created = OrderItem.objects.get_or_create(order=order, product=product)

        if created:
            item.quantity = quantity
        else:
            item.quantity += quantity

        item.save()

        return Response(
            {
                'message': f'{item.quantity} x {product.name} añadido al carrito',
                'order_id': order.id,
                'item_id': item.id,
            },
            status=status.HTTP_200_OK
        )


# ---------------------------------------------------------
# 🛒 Ver carrito actual
# ---------------------------------------------------------
class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        order = get_or_create_active_order(request.user)
        items = order.items.all()
        serializer = CartItemSerializer(items, many=True)
        return Response(serializer.data)


# ---------------------------------------------------------
# ✏️ Actualizar item del carrito
# ---------------------------------------------------------
class CartItemUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            order = get_or_create_active_order(request.user)
            item = order.items.get(pk=pk)
        except OrderItem.DoesNotExist:
            return Response({"detail": "Item no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        quantity = request.data.get("quantity")

        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            quantity = None

        if quantity and quantity > 0:
            item.quantity = quantity
            item.save()
            return Response(
                {"message": f"{item.quantity} x {item.product.name} actualizado"},
                status=status.HTTP_200_OK
            )

        return Response({"detail": "Cantidad inválida"}, status=status.HTTP_400_BAD_REQUEST)


# ---------------------------------------------------------
# ❌ Eliminar item
# ---------------------------------------------------------
class CartItemDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            order = get_or_create_active_order(request.user)
            item = order.items.get(pk=pk)
        except OrderItem.DoesNotExist:
            return Response({"detail": "Item no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        product_name = item.product.name
        item.delete()

        return Response({"message": f"{product_name} eliminado del carrito"}, status=status.HTTP_200_OK)


# ---------------------------------------------------------
# 📄 Resumen del pedido
# ---------------------------------------------------------
class OrderSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            order = Order.objects.get(pk=pk, user=request.user)
        except Order.DoesNotExist:
            return Response({"detail": "Pedido no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        items = order.items.all()
        total = sum(item.total_price for item in items)

        data = {
            "order_id": order.id,
            "items": [
                {
                    "product": item.product.name,
                    "price": float(item.product.price),
                    "quantity": item.quantity,
                    "subtotal": float(item.total_price),
                }
                for item in items
            ],
            "total": float(total),
        }

        return Response(data)


# ---------------------------------------------------------
# 💳 Checkout: Completar pago
# ---------------------------------------------------------
class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            order = Order.objects.get(pk=pk, user=request.user)
        except Order.DoesNotExist:
            return Response({"detail": "Pedido no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        if order.is_paid or order.status == Order.STATUS_PAID:
            return Response({"detail": "Este pedido ya está pagado"}, status=status.HTTP_400_BAD_REQUEST)

        order.is_paid = True
        order.status = Order.STATUS_PAID
        order.save()

        return Response(
            {
                "message": "Pago completado",
                "order_id": order.id,
                "total": float(order.total_price),
            },
            status=status.HTTP_200_OK
        )


# ---------------------------------------------------------
#  Página HTML del carrito
# ---------------------------------------------------------
def cart_page(request):
    return render(request, "cart.html")

class InvoicePDFView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            order = Order.objects.get(pk=pk, user=request.user, is_paid=True)
        except Order.DoesNotExist:
            return Response(
                {"detail": "Pedido no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="factura_pedido_{order.id}.pdf"'

        p = canvas.Canvas(response, pagesize=A4)
        width, height = A4

        #  Cabecera
        p.setFont("Helvetica-Bold", 16)
        p.drawString(2 * cm, height - 2 * cm, "FACTURA")

        p.setFont("Helvetica", 10)
        p.drawString(2 * cm, height - 3 * cm, f"Pedido nº: {order.id}")
        p.drawString(2 * cm, height - 3.6 * cm, f"Fecha: {order.created_at.strftime('%d/%m/%Y')}")
        p.drawString(2 * cm, height - 4.2 * cm, f"Cliente: {order.user.username}")

        #  Tabla de productos
        y = height - 6 * cm

        p.setFont("Helvetica-Bold", 10)
        p.drawString(2 * cm, y, "Producto")
        p.drawString(10 * cm, y, "Cantidad")
        p.drawString(13 * cm, y, "Precio")
        p.drawString(16 * cm, y, "Subtotal")

        y -= 0.5 * cm
        p.line(2 * cm, y, width - 2 * cm, y)

        p.setFont("Helvetica", 10)

        for item in order.items.all():
            y -= 0.8 * cm
            p.drawString(2 * cm, y, item.product.name)
            p.drawString(10 * cm, y, str(item.quantity))
            p.drawString(13 * cm, y, f"{item.product.price} €")
            p.drawString(16 * cm, y, f"{item.total_price} €")

            if y < 2 * cm:
                p.showPage()
                y = height - 2 * cm

        #  Total
        y -= 1 * cm
        p.setFont("Helvetica-Bold", 12)
        p.drawString(13 * cm, y, "TOTAL:")
        p.drawString(16 * cm, y, f"{order.total_price} €")

        p.showPage()
        p.save()

        return response
