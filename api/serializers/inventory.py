from rest_framework import serializers
from api.models import Inventory, Furniture

class InventorySerializer(serializers.ModelSerializer):
    furniture = serializers.PrimaryKeyRelatedField(queryset=Furniture.objects.all())  # ✅ Correct way

    class Meta:
        model = Inventory
        fields = ['id', 'furniture', 'quantity']
