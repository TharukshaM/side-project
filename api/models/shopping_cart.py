from django.db import models
from .user import CustomUser
from .furniture import Furniture

class ShoppingCart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="cart")
    furniture = models.ForeignKey(Furniture, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    class Meta:
        unique_together = ('user', 'furniture')  # Prevent duplicate entries for the same item.

    def total_price(self):
        """Calculate total price of this item in cart."""
        return self.furniture.price * self.quantity

    def __str__(self):
        return f"{self.user.username}'s cart - {self.furniture.name} (x{self.quantity})"
