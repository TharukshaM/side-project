from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from api.models.inventory import Inventory
from api.models.furniture import Furniture
from rest_framework.authtoken.models import Token

User = get_user_model()

class TestInventoryAPI(APITestCase):  # ✅ Class name should start with "Test"

    def setUp(self):
        """✅ Create a test user and sample furniture for testing."""
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="password123")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')  # ✅ Authenticate requests

        # ✅ Ensure furniture is created before inventory
        self.furniture = Furniture.objects.create(
            name="Wooden Chair",
            description="A durable wooden chair",
            category="chair",
            price=150.00,
            dimensions="50x50x100 cm"
        )

        # ✅ Create inventory using the Furniture instance (not furniture_id)
        self.inventory = Inventory.objects.create(
            furniture=self.furniture,  # ✅ Pass the object, not the ID
            quantity=10
        )

    def test_create_inventory(self):
        """✅ Test adding inventory for a furniture item"""
        url = "/inventory/"
        data = {
            "furniture": self.furniture.id,  # ✅ Ensure correct furniture ID
            "quantity": 5
        }
        print(f"Furniture ID in test: {self.furniture.id}")  # Debugging
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["furniture"], self.furniture.id)
        self.assertEqual(response.data["quantity"], 5)

    def test_get_inventory_list(self):
        """✅ Test retrieving all inventory items"""
        url = "/inventory/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)  # ✅ Check 200 OK
        self.assertGreater(len(response.data), 0)

    def test_get_single_inventory(self):
        """✅ Test retrieving a single inventory item"""
        url = f"/inventory/{self.inventory.id}/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["quantity"], 10)

    def test_update_inventory_quantity(self):
        """✅ Test updating inventory quantity"""
        url = f"/inventory/{self.inventory.id}/"
        data = {"quantity": 25}
        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["quantity"], 25)

    def test_update_inventory_negative_quantity(self):
        """✅ Test setting a negative inventory quantity (should fail)"""
        url = f"/inventory/{self.inventory.id}/"
        data = {"quantity": -5}
        response = self.client.patch(url, data, format="json")

        print("RESPONSE DATA when update with negative quanity :", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Ensure this value is greater than or equal to 0.", str(response.data))

    def test_delete_inventory(self):
        """✅ Test deleting an inventory item"""
        url = f"/inventory/{self.inventory.id}/"
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_search_furniture_by_name(self):
        """✅ Test searching furniture by name"""
        url = "/inventory/search/?name=Wooden Chair"  # ✅ Ensure correct query
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)  # ✅ Ensure at least one result

    def test_search_furniture_by_category(self):
        """✅ Test searching furniture by category"""
        url = "/inventory/search/?category=chair"  # ✅ Use query parameters correctly
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)  # ✅ Ensure results are returned

    def test_search_furniture_by_price_range(self):
        """✅ Test searching furniture within a price range"""
        url = "/inventory/search/?min_price=100&max_price=200"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_search_furniture_no_results(self):
        """✅ Test searching furniture that does not exist"""
        url = "/inventory/search/?name=Nonexistent"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # ✅ Expecting no results
