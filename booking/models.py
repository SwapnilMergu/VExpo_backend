from django.db import models
from stalls.models import Stalls
from visitors.models import Visitors

# Create your models here.
class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    stall = models.ForeignKey(Stalls, on_delete=models.CASCADE, default=None)
    visitor = models.ForeignKey(Visitors, on_delete=models.CASCADE)
    date = models.TextField(default='')
    time = models.TextField(default='')
    interest = models.TextField(default='')
    status = models.CharField(max_length=255, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'booking'