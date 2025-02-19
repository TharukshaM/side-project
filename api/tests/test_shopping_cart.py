from django.test import TestCase
from django.contrib.auth import get_user_model
from api.models.furniture import Furniture
from api.models.shopping_cart import ShoppingCart

User = get_user_model()

class ShoppingCartTestCase(TestCase):
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="password123")
        self.furniture = Furniture.objects.create(name="Wooden Table", category="table", price=200.00, stock=5)
        self.cart_item = ShoppingCart.objects.create(user=self.user, furniture=self.furniture, quantity=2)

    def test_cart_total_price(self):
        """Test total price calculation."""
        self.assertEqual(self.cart_item.total_price(), 400.00)

    def test_discount_application(self):
        """Test applying a discount."""
        discount = 10  # 10% off
        discounted_price = self.furniture.calculate_discount(discount)
        self.assertEqual(discounted_price, 180.00)
