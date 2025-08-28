from django.urls import path,include
from rest_framework.routers import DefaultRouter
from equipments.views import *

router = DefaultRouter()
router.register(r'categories',CategoryViewSet)
router.register(r'equipments',EquipmentViewSet)

urlpatterns = [
    path('', include(router.urls))
]