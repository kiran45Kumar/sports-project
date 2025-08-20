from django.shortcuts import render
from rest_framework import viewsets
from .models import Users
# Create your views here.
from .serializers import UsersSerializer

class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer

    