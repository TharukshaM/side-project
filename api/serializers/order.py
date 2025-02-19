from rest_framework import serializers
from api.models.order import Order, OrderItem
from api.models.furniture import Furniture

class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for OrderItem model."""
    furniture = serializers.StringRelatedField()

    class Meta:
        model = OrderItem
        fields = ['id', 'furniture', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for Order model."""
    items = OrderItemSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'total_price', 'payment_method', 'status', 'address', 'created_at', 'items']
