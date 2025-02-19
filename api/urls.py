from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FurnitureViewSet, OrderViewSet

router = DefaultRouter()
router.register(r'furniture', FurnitureViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
