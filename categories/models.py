from django.db import models

# Create your models here.

class Categories(models.Model):
    cname = models.CharField(max_length=255)
    admin_id = models.IntegerField(null=True,default=None,blank=True)
    superuser_id = models.IntegerField(null=True,default=None,blank=True)
    status = models.CharField(max_length=255, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.cname
    
    class Meta:
        db_table = 'categories'