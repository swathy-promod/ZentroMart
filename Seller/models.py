from django.db import models
from Adminstrator.models import*
from Guest.models import*


class tbl_product(models.Model):
        product_name=models.CharField(max_length=200)
        product_details=models.CharField(max_length=200)
        product_photo=models.FileField(upload_to="Assets/ShopDocs/Photo")
        product_price=models.CharField(max_length=200)
        subcategory=models.ForeignKey(tbl_subcategory,on_delete=models.CASCADE)
        shop=models.ForeignKey(tbl_shop,on_delete=models.CASCADE)
        brand=models.ForeignKey(tbl_brand,on_delete=models.CASCADE)

class tbl_gallery(models.Model):
    gallery_file=models.FileField(upload_to="Assets/ShopDocs/Photo")   
    productid=models.ForeignKey(tbl_product,on_delete=models.CASCADE)

class tbl_stock(models.Model):
    stock_quality=models.CharField(max_length=200)
    stock_date=models.DateField(auto_now_add=True)
    productid=models.ForeignKey(tbl_product,on_delete=models.CASCADE)
        