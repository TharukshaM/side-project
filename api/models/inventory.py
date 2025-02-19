from django.db import models
from .furniture import Furniture  # Import Furniture model

class Inventory(models.Model):
    """Inventory class to manage furniture stock."""
    
    furniture = models.OneToOneField(Furniture, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)  # Actual stock count

    def __str__(self):
        return f"{self.furniture.name} - {self.quantity} in stock"

    def add_furniture(self, amount):
        """Increase stock quantity."""
        if amount <= 0:
            raise ValueError("Amount must be greater than zero")
        self.quantity += amount
        self.furniture.stock += amount
        self.furniture.save()
        self.save()

    def remove_furniture(self, amount):
        """Decrease stock quantity, ensuring it doesn't go negative."""
        if amount <= 0:
            raise ValueError("Amount must be greater than zero")
        if amount > self.quantity:
            raise ValueError("Not enough stock available")
        self.quantity -= amount
        self.furniture.stock -= amount
        self.furniture.save()
        self.save()

    def update_furniture_quantity(self, new_quantity):
        """Update furniture stock to a specific number."""
        if new_quantity < 0:
            raise ValueError("Quantity cannot be negative")
        self.quantity = new_quantity
        self.furniture.stock = new_quantity
        self.furniture.save()
        self.save()

    @staticmethod
    def search_furniture(name=None, category=None, min_price=None, max_price=None):
        """Search for furniture based on attributes."""
        queryset = Furniture.objects.all()

        if name:
            queryset = queryset.filter(name__icontains=name)
        if category:
            queryset = queryset.filter(category=category)
        if min_price is not None:
            queryset = queryset.filter(price__gte=min_price)
        if max_price is not None:
            queryset = queryset.filter(price__lte=max_price)

        return queryset
