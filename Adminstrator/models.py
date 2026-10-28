from django.db import models

# tbl_district
class tbl_district(models.Model):
    district_name=models.CharField(max_length=30)

# tbl_category
class tbl_category(models.Model):
    Category_name=models.CharField(max_length=30)

# tbl_adminregistration
class tbl_adminregistration(models.Model):
    adminregistration_name=models.CharField(max_length=30)
    adminregistration_contact=models.CharField(max_length=30)
    adminregistration_email=models.CharField(max_length=30)
    adminregistration_password=models.CharField(max_length=30)

# tbl_place
class tbl_place(models.Model):
    place_name=models.CharField(max_length=30)
    district=models.ForeignKey(tbl_district,on_delete=models.CASCADE)
    place_pin=models.CharField(max_length=20)

# tbl_subcatgeory
class tbl_subcategory(models.Model):
    subcategory_name=models.CharField(max_length=30)
    Category_name=models.ForeignKey(tbl_category,on_delete=models.CASCADE)


class tbl_brand(models.Model):
    brand_name=models.CharField(max_length=30)