from rest_framework import serializers
from equipments.models import *

class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipments
        fields = "__all__"

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"