import pytest
from rest_framework.test import APIClient
from api.models.furniture import Furniture
from api.models.order import Order
from api.models.shopping_cart import ShoppingCart
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_full_order_process():
    
    client = APIClient()

    # Register a User
    response = client.post("/auth/register/", {
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123",
        "address": "123 Main Street"
    })
    assert response.status_code == 201

    # Login User
    response = client.post("/auth/login/", {
        "username": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    token = response.data["token"]

    # Authenticate user for further requests
    client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

    # Create Furniture Item
    response = client.post("/furniture/", {
        "name": "Dining Table",
        "description": "Luxury Wooden Dining Table",
        "category": "table",
        "price": 300.00,
        "dimensions": "180x90x80 cm",
        "stock": 10
    }, format="json")
    assert response.status_code == 201
    furniture_id = response.data["id"]

    # Add Item to Shopping Cart
    response = client.post("/shopping-cart/", {
        "furniture_id": furniture_id,
        "quantity": 2
    }, format="json")
    assert response.status_code == 201

    # Validate Total Price
    response = client.get("/shopping-cart/total_price/")
    assert response.status_code == 200
    assert response.data["total_price"] == 600.00  # 2 * 300

    # Checkout & Place Order
    response = client.post("/checkout/checkout/", {
        "payment_method": "card",
        "address": "123 Main Street"
    })
    assert response.status_code == 201
    order_id = response.data["order_id"]

    # Ensure Inventory Updates
    furniture = Furniture.objects.get(id=furniture_id)
    assert furniture.stock == 8  # Stock reduced by 2

    # Ensure Order Exists
    order = Order.objects.get(id=order_id)
    assert order.status == "pending"
    assert order.total_price == 600.00

    # Ensure Shopping Cart is Cleared
    assert ShoppingCart.objects.filter(user=order.user).count() == 0

    # Update Order Status (Admin Action)
    response = client.post(f"/order/{order_id}/update_status/", {
        "status": "shipped"
    })
    assert response.status_code == 403  # Normal users can't update orders

    # Authenticate as Admin
    admin = User.objects.create_superuser(username="admin", email="admin@test.com", password="admin123")
    client.force_authenticate(user=admin)



