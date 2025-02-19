from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterUserView, LoginUserView, UserProfileView
from .views import FurnitureViewSet
from .views import InventoryViewSet
from .views import CheckoutViewSet
from .views import OrderViewSet
from .views.shopping_cart import ShoppingCartViewSet
from .views.inventory import InventorySearchView
from api.views.inventory import InventoryViewSet

router = DefaultRouter()
router.register(r'furniture', FurnitureViewSet, basename='furniture')
router.register(r'inventory', InventoryViewSet, basename='inventory')
router.register(r'shopping-cart', ShoppingCartViewSet, basename='shopping-cart')
router.register(r'checkout', CheckoutViewSet, basename='checkout')
router.register(r'order', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', RegisterUserView.as_view(), name='register'),
    path('auth/login/', LoginUserView.as_view(), name='login'),
    path('auth/profile/', UserProfileView.as_view(), name='profile'),
    path('inventory/search/', InventoryViewSet.as_view({'get': 'search'}), name='inventory-search'),  # ✅ Add search endpoint
]
