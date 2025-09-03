from django.db import models
from users.models import Users 
from equipments.models import Equipments
# Create your models here.

class Booking(models.Model):
    bid = models.AutoField(primary_key=True)
    equipment = models.ForeignKey(Equipments, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='booking_photos/', null=True, blank=True) #user photo with equipment.
    booking_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    