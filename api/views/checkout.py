from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from api.models.order import Order, OrderItem
from api.models.shopping_cart import ShoppingCart
from api.models.inventory import Inventory
from api.serializers.order import OrderSerializer
from decimal import Decimal

class CheckoutViewSet(viewsets.ViewSet):
    """API ViewSet for handling Checkout."""
    
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['POST'])
    def checkout(self, request):
        """Creates an order from the user's shopping cart."""
        user = request.user
        cart_items = ShoppingCart.objects.filter(user=user)

        if not cart_items.exists():
            return Response({"error": "Your cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

        address = request.data.get("address")
        payment_method = request.data.get("payment_method")

        if not address or not payment_method:
            return Response({"error": "Address and payment method are required."}, status=status.HTTP_400_BAD_REQUEST)

        total_price = sum(item.furniture.price * item.quantity for item in cart_items)

        # Create order
        order = Order.objects.create(
            user=user,
            total_price=total_price,
            payment_method=payment_method,
            address=address,
            status="pending"
        )

        # Create order items & update inventory
        for cart_item in cart_items:
            inventory = Inventory.objects.get(furniture=cart_item.furniture)
            
            if cart_item.quantity > inventory.quantity:
                return Response(
                    {"error": f"Not enough stock for {cart_item.furniture.name}."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            OrderItem.objects.create(
                order=order,
                furniture=cart_item.furniture,
                quantity=cart_item.quantity,
                price=cart_item.furniture.price,
            )

            # Update inventory
            inventory.quantity -= cart_item.quantity
            inventory.save()

        # Clear user's shopping cart
        cart_items.delete()

        #This is for check commit comment by 

        return Response({"message": "Order placed successfully!", "order_id": order.id}, status=status.HTTP_201_CREATED)
