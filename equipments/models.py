from django.db import models
from users.models import Users
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    desc = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
class Equipments(models.Model):
    status_choices = [
        ('approved','Approved'),
        ('rejected','Rejected'),
        ('pending','Pending'),
        ('blocked', 'Blocked'),
    ]
    type_choices = [
        ('hour', 'Hourly'),
        ('day', 'Daily'),
        ('week', 'Weekly'),
        ('month', 'Monthly'),
    ]
    eid = models.AutoField(primary_key=True)
    e_name = models.CharField(max_length=20, null=False, blank=False)
    e_description = models.TextField(null=False, blank=False)
    e_price = models.DecimalField(max_digits=5, decimal_places=2,null=False, blank=False)
    e_deposit = models.DecimalField(max_digits=10, decimal_places=2,null=False, blank=False,default="This amount is refundable after the return of product.")
    e_quantity = models.IntegerField(null=False, blank=False)
    etype = models.CharField(max_length=20, null=False, blank=False, default='', choices=type_choices)
    e_status = models.CharField(max_length=10, blank=False, null=False, default="pending",choices=status_choices)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user_posted = models.ForeignKey(Users, on_delete=models.CASCADE)
    e_created = models.DateTimeField(auto_now_add=True)
    e_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.e_name

class EquipmentImage(models.Model):
    equipment = models.ForeignKey(Equipments, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='equipment_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)