from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    desc = models.TextField(max_length=50)
    mobNo = models.IntegerField()

    def __str__(self):
        return self.name
    
class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, default="")
    sub_category = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=300)
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return self.product_name
    

class Orders(models.Model):
    order_id = models.AutoField(models.AutoField, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    items_json =  models.CharField(max_length=5000)
    amount = models.IntegerField(default=0)
    name = models.CharField(max_length=90)
    email = models.CharField(max_length=90)
    address1 = models.CharField(max_length=200)
    address2 = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)
    oid=models.CharField(max_length=50,blank=True)
    paymentstatus=models.CharField(max_length=20,blank=True)
    orderStatus = models.CharField(max_length=50, default="Not Delivered")
    phone = models.CharField(max_length=100,default="")
    date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)
    def __str__(self):
        return self.name


class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default=0)
    update_desc = models.CharField(max_length=5000, null=True)
    new_update_desc = models.CharField(max_length=5000, null=True)
    delivered = models.BooleanField(default=False)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7] + "..."