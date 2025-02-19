from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from api.models.order import Order
from api.serializers.order import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    """API ViewSet for handling Orders."""
    
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve orders for the logged-in user."""
        return Order.objects.filter(user=self.request.user)

    @action(detail=True, methods=['POST'], permission_classes=[IsAdminUser])
    def update_status(self, request, pk=None):
        """Allows updating an order's status (Admin Only)."""
        order = self.get_object()
        new_status = request.data.get("status")

        if new_status not in ["pending", "shipped", "delivered", "cancelled"]:
            return Response({"error": "Invalid status."}, status=status.HTTP_400_BAD_REQUEST)

        order.status = new_status
        order.save()
        return Response({"message": f"Order status updated to {new_status}."}, status=status.HTTP_200_OK)
