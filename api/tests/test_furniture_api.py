from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from api.models.furniture import Furniture

User = get_user_model()

class FurnitureAPITestCase(APITestCase):
    """Test the Furniture API endpoints"""

    def setUp(self):
        """ Create a test user for authentication"""
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="password123")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        #  Create a test furniture item
        self.furniture = Furniture.objects.create(
            name="Wooden Chair",
            description="A durable wooden chair",
            category="Chair",
            price=100.0,
            dimensions="40x40x90 cm"
        )

    def test_create_furniture(self):
        """ Test creating a furniture item"""
        url = "/furniture/"
        data = {
            "name": "New Sofa",
            "description": "A comfortable sofa",
            "category": "sofa",
            "price": 250.00,
            "dimensions": "180x90x80 cm"
        }
        response = self.client.post(url, data, format="json")

        print("RESPONSE DATA:", response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  #  Check 201 Created
        self.assertEqual(response.data["name"], "New Sofa")

    def test_get_furniture_list(self):
        """ Test retrieving all furniture items"""
        url = "/furniture/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)  #  Check 200 OK
        self.assertGreater(len(response.data), 0)

    def test_get_single_furniture(self):
        """ Test retrieving a single furniture item"""
        url = f"/furniture/{self.furniture.id}/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)  #  Check 200 OK
        self.assertEqual(response.data["name"], "Wooden Chair")

    def test_update_furniture(self):
        """ Test updating a furniture item"""
        url = f"/furniture/{self.furniture.id}/"
        data = {"name": "Updated Wooden Chair"}
        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)  #  Check 200 OK
        self.assertEqual(response.data["name"], "Updated Wooden Chair")

    def test_delete_furniture(self):
        """ Test deleting a furniture item"""
        url = f"/furniture/{self.furniture.id}/"
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)  #  Check 204 No Content
