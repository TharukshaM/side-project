from rest_framework import serializers
from api.models.inventory import Inventory
from api.serializers.furniture import FurnitureSerializer

class InventorySerializer(serializers.ModelSerializer):
    """Serializer for Inventory model."""
    
    furniture = FurnitureSerializer(read_only=True)

    class Meta:
        model = Inventory
        fields = ['id', 'furniture', 'quantity']
