from django.db import models
from admin_profile.models import AdminProfile
from visitors.models import Visitors

# Create your models here.
class Registration(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.ForeignKey(AdminProfile, on_delete=models.CASCADE, default=None)
    visitor = models.ForeignKey(Visitors, on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'registration'