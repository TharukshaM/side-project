from django.db import models

class Furniture(models.Model):
    CATEGORY_CHOICES = [
        ('chair', 'Chair'),
        ('sofa', 'Sofa'),
        ('table', 'Table'),
        ('bed', 'Bed'),
        ('cabinet', 'Cabinet'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    dimensions = models.CharField(max_length=100, help_text="Example: 100x50x40 cm")
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.category})"

    def calculate_discount(self, percentage):
        """Apply a discount and return the new price."""
        discount_amount = (percentage / 100) * self.price
        return round(self.price - discount_amount, 2)

    def apply_tax(self, tax_rate=10):
        """Apply a tax percentage to the price."""
        tax_amount = (tax_rate / 100) * self.price
        return round(self.price + tax_amount, 2)

    def check_availability(self):
        """Check if the furniture is available in stock."""
        return self.stock


class Inventory(models.Model):
    """Inventory class to manage furniture stock."""
    
    furniture = models.OneToOneField("Furniture", on_delete=models.CASCADE)
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