from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from api.models.inventory import Inventory
from api.serializers.inventory import InventorySerializer

class InventoryViewSet(viewsets.ModelViewSet):
    """ViewSet for managing Inventory."""

    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

    @action(detail=True, methods=['POST'])
    def add_furniture(self, request, pk=None):
        """Add stock to inventory."""
        inventory = self.get_object()
        amount = int(request.data.get('amount', 0))
        if amount > 0:
            inventory.add_furniture(amount)
            return Response({"message": f"Added {amount} units to inventory."})
        return Response({"error": "Amount must be greater than zero"}, status=400)

    @action(detail=True, methods=['POST'])
    def remove_furniture(self, request, pk=None):
        """Remove stock from inventory."""
        inventory = self.get_object()
        amount = int(request.data.get('amount', 0))
        try:
            inventory.remove_furniture(amount)
            return Response({"message": f"Removed {amount} units from inventory."})
        except ValueError as e:
            return Response({"error": str(e)}, status=400)

    @action(detail=True, methods=['POST'])
    def update_quantity(self, request, pk=None):
        """Update stock quantity."""
        inventory = self.get_object()
        new_quantity = int(request.data.get('new_quantity', 0))
        try:
            inventory.update_furniture_quantity(new_quantity)
            return Response({"message": f"Updated inventory quantity to {new_quantity}."})
        except ValueError as e:
            return Response({"error": str(e)}, status=400)

    @action(detail=False, methods=['GET'])
    def search_furniture(self, request):
        """Search for furniture based on attributes."""
        name = request.query_params.get('name')
        category = request.query_params.get('category')
        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')

        results = Inventory.search_furniture(name, category, min_price, max_price)
        serializer = self.get_serializer(results, many=True)
        return Response(serializer.data)
