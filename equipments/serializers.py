from rest_framework import serializers
from equipments.models import *

class EquipmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Equipments
        fields = ['url','eid', 'e_name', 'e_description', 'e_price', 'e_deposit', 'e_quantity', 'etype', 'e_status', 'category', 'user_posted', 'e_created', 'e_updated', ]

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name','desc', 'created_at', 'updated_at','url']