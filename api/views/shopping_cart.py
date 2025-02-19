from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from api.models.shopping_cart import ShoppingCart
from api.serializers.shopping_cart import ShoppingCartSerializer
from api.models.discount import PercentageDiscount, FixedAmountDiscount

class ShoppingCartViewSet(viewsets.ModelViewSet):
    """API endpoints for managing the shopping cart."""
    serializer_class = ShoppingCartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter the cart to only show items for the authenticated user."""
        return ShoppingCart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Ensure the cart entry is linked to the authenticated user."""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['GET'])
    def total_price(self, request):
        """Get the total price of all items in the cart."""
        cart_items = self.get_queryset()
        total = sum(item.total_price() for item in cart_items)
        return Response({"total_price": total}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'])
    def apply_discount(self, request, pk=None):
        """Apply a discount using a strategy pattern."""
        cart_item = self.get_object()
        discount_type = request.data.get("type", "percentage")  # Default: percentage
        amount = float(request.data.get("amount", 10))  # Default: 10%

        if discount_type == "percentage":
            discount_strategy = PercentageDiscount(amount)
        elif discount_type == "fixed":
            discount_strategy = FixedAmountDiscount(amount)
        else:
            return Response({"error": "Invalid discount type."}, status=status.HTTP_400_BAD_REQUEST)

        discounted_price = discount_strategy.apply_discount(cart_item.furniture.price)
        return Response({"discounted_price": discounted_price}, status=status.HTTP_200_OK)
