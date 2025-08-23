from django.db import models
from django.core.validators import FileExtensionValidator
# Create your models here.
#Model for both register and login.
def validate_fields(value):
    if not value:
        raise ValueError("This field cannot be empty")
    return value
class Users(models.Model):
    status_choices = [
        ('approved','Approved'),
        ('rejected','Rejected'),
        ('pending','Pending'),
    ]
    #user details
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=50, null=True, blank=True, validators=[validate_fields])
    user_email = models.EmailField(max_length=70, null=False, blank=False, unique=True, validators=[validate_fields])
    user_pass = models.CharField(max_length=20, null=False, blank=False, validators=[validate_fields])
    user_phone = models.CharField(null=False, blank=False, max_length=15, unique=True, validators=[validate_fields])
    user_address = models.CharField(max_length=350, null=True, blank=True, validators=[validate_fields])
    user_city = models.CharField(max_length=50, null=True, blank=True, validators=[validate_fields])
    user_state = models.CharField(max_length=50, null=True, blank=True, validators=[validate_fields])
    user_country = models.CharField(max_length=50, null=True, blank=True, validators=[validate_fields])
    user_zip = models.CharField(max_length=10, null=True, blank=True, validators=[validate_fields])
    #user identification
    user_aadhar = models.CharField(max_length=12, null=False, blank=False, validators=[validate_fields])
    adhar_file = models.FileField(upload_to='adhar_files/',null=False,blank=False, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    #user profile picture
    user_profile_picture = models.ImageField(upload_to='user_profiles/',null=False, blank=True, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])
    user_approval = models.BooleanField(default=False)
    user_status = models.CharField(max_length=10, choices=status_choices, default='pending')
    message = models.TextField(null=True, blank=True, default="Rejection reason messages")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user_name
    

