from rest_framework import serializers
from api.models.inventory import Inventory

class InventorySerializer(serializers.ModelSerializer):
    """Serializer for Inventory model."""

    furniture = serializers.SerializerMethodField()  # Use method field to avoid direct import

    class Meta:
        model = Inventory
        fields = ['id', 'furniture', 'quantity']

    def get_furniture(self, obj):
        """Dynamically import FurnitureSerializer to avoid circular import."""
        from api.serializers.furniture import FurnitureSerializer
        return FurnitureSerializer(obj.furniture).data
