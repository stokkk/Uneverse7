from django.db import models

# Create your models here.


class MyModel(models.Model):
    class Meta:
        managed = False
        verbose_name = "Add products"


class Product(models.Model):
    class Meta:
        managed = False
        verbose_name = "Product"

class IGBTs(Product):
    class Meta:
        managed = False
        verbose_name = "IGBTs"