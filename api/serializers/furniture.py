from rest_framework import serializers
from api.models.furniture import Furniture

class FurnitureSerializer(serializers.ModelSerializer):
    """Serializer for Furniture model."""

    discounted_price = serializers.SerializerMethodField()
    price_with_tax = serializers.SerializerMethodField()

    class Meta:
        model = Furniture
        fields = ['id', 'name', 'description', 'category', 'price', 'dimensions', 'stock', 'created_at', 
                  'discounted_price', 'price_with_tax']
    
    def get_discounted_price(self, obj):
        """Applies a default 10% discount."""
        return obj.calculate_discount(10)

    def get_price_with_tax(self, obj):
        """Applies the default 10% tax rate."""
        return obj.apply_tax(10)
