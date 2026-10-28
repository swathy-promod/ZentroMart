from django.db import models
from Adminstrator.models import *

# tbl_user
class tbl_user(models.Model):
    place=models.ForeignKey(tbl_place,on_delete=models.CASCADE)
    user_gender=models.CharField(max_length=30)  
    user_name=models.CharField(max_length=30)
    user_contact=models.CharField(max_length=30)
    user_email=models.CharField(max_length=30)
    user_password=models.CharField(max_length=30)
    user_address=models.CharField(max_length=30)
    user_photo=models.FileField(upload_to="Assets/User/Photo")
    user_proof=models.FileField(upload_to="Assets/User/Photo")
    user_status=models.IntegerField(default=0)

# shopregistrat
class tbl_shop(models.Model):
    place=models.ForeignKey(tbl_place,on_delete=models.CASCADE)
    shop_name=models.CharField(max_length=30)
    shop_contact=models.CharField(max_length=30)
    shop_email=models.CharField(max_length=30)
    shop_password=models.CharField(max_length=30)
    shop_address=models.CharField(max_length=30)
    shop_photo=models.FileField(upload_to="Assets/ShopDocs/Photo")
    shop_proof=models.FileField(upload_to="Assets/ShopDocs/Photo")
    shop_status=models.IntegerField(default=0)

class tbl_dboy(models.Model):
    place=models.ForeignKey(tbl_place,on_delete=models.CASCADE)
    dboy_name=models.CharField(max_length=30)
    dboy_contact=models.CharField(max_length=30)
    dboy_email=models.CharField(max_length=30)
    dboy_password=models.CharField(max_length=30)
    dboy_address=models.CharField(max_length=30)
    dboy_photo=models.FileField(upload_to="Assets/ShopDocs/Photo")
    dboy_proof=models.FileField(upload_to="Assets/ShopDocs/Photo")
    dboy_status=models.IntegerField(default=0)
    
