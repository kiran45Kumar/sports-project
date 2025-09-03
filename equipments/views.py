from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from equipments.models import *
from equipments.serializers import *
# Create your views here.
class EquipmentViewSet(ModelViewSet):
    queryset = Equipments.objects.all().order_by('-e_created')
    serializer_class = EquipmentSerializer

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all().order_by('-created_at')
    serializer_class = CategorySerializer



