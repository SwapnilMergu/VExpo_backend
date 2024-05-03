from django.db import models
from visitors.models import Visitors
from stalls.models import Stalls

# Create your models here.
class Visits(models.Model):
    id = models.AutoField(primary_key=True)
    visitors = models.ForeignKey(Visitors, on_delete=models.CASCADE)
    stalls = models.ForeignKey(Stalls, on_delete=models.CASCADE)
    rating = models.IntegerField(null=True,default=None,blank=True)
    review = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table='visits'