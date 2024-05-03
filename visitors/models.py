from django.db import models
from django.contrib.auth.hashers import make_password


# Create your models here.
class Visitors(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=False,null=True,blank=True)
    contact = models.CharField(unique=True,max_length=15)
    company = models.CharField(max_length=100,default='')
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table='visitors'

    # def check_password(self, password):
    #     print('self.password : ',self.password)
    #     print('password : ',password)

    #     print('make_password(password) : ',make_password(password))
    #     print('make_password(rahul) : ',make_password('rahul'))
    #     print('make_password(rahul) : ',make_password('rahul'))
    #     print('self.password == make_password(password) : ',self.password == make_password(password))
    #     return self.password == make_password(password)