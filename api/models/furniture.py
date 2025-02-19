from django.db import models
from decimal import Decimal

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
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.category})"

    def calculate_discount(self, percentage):
        """Apply a discount and return the new price."""
        percentage_decimal = Decimal(str(percentage)) / Decimal("100")
        discount_amount = percentage_decimal * self.price
        return round(self.price - discount_amount, 2)

    def apply_tax(self, tax_rate=10):
        """Apply a tax percentage to the price."""
        tax_decimal = Decimal(str(tax_rate)) / Decimal("100")
        tax_amount = tax_decimal * self.price
        return self.price + tax_amount
