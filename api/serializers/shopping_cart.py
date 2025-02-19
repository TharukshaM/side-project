from rest_framework import serializers
from api.models.shopping_cart import ShoppingCart
from api.models.furniture import Furniture 
from api.serializers.furniture import FurnitureSerializer

class ShoppingCartSerializer(serializers.ModelSerializer):
    furniture = FurnitureSerializer(read_only=True) 
    furniture_id = serializers.PrimaryKeyRelatedField(queryset=Furniture.objects.all(), source="furniture", write_only=True)

    class Meta:
        model = ShoppingCart
        fields = ['id', 'user', 'furniture', 'furniture_id', 'quantity', 'total_price']
        extra_kwargs = {'user': {'read_only': True}}
    
    def validate_quantity(self, value):
        """Ensure quantity is a positive integer."""
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1.")
        return value
