from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from equipments.models import *
from equipments.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
class EquipmentViewSet(ModelViewSet):
    queryset = Equipments.objects.all().order_by('-e_created')
    serializer_class = EquipmentSerializer

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all().order_by('-created_at')
    serializer_class = CategorySerializer


class ViewAllEquipments(APIView):
    def get(self, request):
        equipments = Equipments.objects.all().order_by('-e_created')
        eq_arr = []
        for eq in equipments:
            eq_arr.append({
                "id": eq.eid,
                "name": eq.e_name,
                "description": eq.e_description,
                "price": eq.e_price,
                "deposit": eq.e_deposit,
                "quantity": eq.e_quantity,
                "type": eq.etype,
                "status": eq.e_status,
                "category": eq.category.name if eq.category else None,
                "user_posted": eq.user_posted.user_name if eq.user_posted else None,
                "created": eq.e_created,
                "updated": eq.e_updated,
            })
        return Response({"all_equipments": eq_arr}, status=status.HTTP_200_OK)
