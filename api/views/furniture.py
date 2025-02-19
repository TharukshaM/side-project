from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from api.models.furniture import Furniture
from api.serializers.furniture import FurnitureSerializer

class FurnitureViewSet(viewsets.ModelViewSet):
    """ViewSet for managing Furniture items."""
    
    queryset = Furniture.objects.all()
    serializer_class = FurnitureSerializer

    @action(detail=True, methods=['POST'])
    def apply_discount(self, request, pk=None):
        """Apply a discount to the furniture item."""
        furniture = self.get_object()
        discount = float(request.data.get('discount', 10))  # Default to 10%
        new_price = furniture.calculate_discount(discount)
        return Response({"discounted_price": new_price})

    @action(detail=True, methods=['POST'])
    def apply_tax(self, request, pk=None):
        """Apply a tax rate to the furniture item."""
        furniture = self.get_object()
        tax_rate = float(request.data.get('tax_rate', 10))  # Default to 10%
        price_with_tax = furniture.apply_tax(tax_rate)
        return Response({"price_with_tax": price_with_tax})
