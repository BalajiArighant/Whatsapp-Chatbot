from django.db import models

# Create your models here.

class User(models.Model):
    user_id = models.BigAutoField(primary_key=True)
    user_name = models.CharField(max_length=100, null=True)
    phone_number = models.CharField(max_length=100, null=True)
    kovil = models.CharField(max_length=100, null=True)
    native_place = models.CharField(max_length=100, null=True)
    current_location = models.CharField(max_length=100, null=True)
    booth_collection = models.CharField(max_length=100, null=True)
    token_number = models.IntegerField(null=True)