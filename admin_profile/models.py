from django.db import models
from categories.models import Categories

# Create your models here.
class AdminProfile(models.Model):
    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=100)
    event_name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    address = models.TextField(default='')
    logo = models.TextField(default='')
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, default=None) #models.CharField(max_length=255)
    catalog = models.CharField(max_length=255)
    banner = models.CharField(max_length=255,default='')
    DOB = models.TextField(default='')
    start_date = models.TextField(default='')
    end_date = models.TextField(default='')
    price = models.TextField(default='')
    whatsapp_no = models.TextField(default='')
    social_links = models.TextField(default='')
    status = models.IntegerField(default=0)
    about = models.TextField(default="")
    city = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.event_name

    class Meta:
        db_table = 'admin_profile'