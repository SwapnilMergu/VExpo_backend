from django.db import models
from admin_profile.models import AdminProfile

# Create your models here.
class VendorProfile(models.Model):
    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    contact = models.CharField(max_length=15)
    password = models.CharField(max_length=255)
    address = models.TextField(default='')
    profile = models.TextField(default='')
    DOB = models.TextField(default='')
    whatsapp_no = models.TextField(default='')
    social_links = models.TextField(default='')
    status = models.IntegerField(default=0)
    rating = models.IntegerField(default=None)
    admin = models.ForeignKey(AdminProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'vendor_profile'