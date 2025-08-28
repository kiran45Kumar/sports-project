from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from equipments.models import *
from equipments.serializers import *
# Create your views here.
class EquipmentViewSet(ModelViewSet):
    queryset = Equipments.objects.all()
    serializer_class = EquipmentSerializer

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer



