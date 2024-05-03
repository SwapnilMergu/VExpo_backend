from django.db import models
from vendor_profile.models import VendorProfile
from categories.models import Categories

# Create your models here.
class Stalls(models.Model):
    id = models.AutoField(primary_key=True)
    stall_name = models.CharField(max_length=255)
    logo = models.CharField(max_length=255)
    about = models.TextField()
    email = models.EmailField(max_length=255)
    contact = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    catalog = models.CharField(max_length=255)
    banner = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    stall_visits = models.IntegerField(default=0)
    rating = models.DecimalField(decimal_places=1,max_digits=2,default=None)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, default=None)
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'stalls'
