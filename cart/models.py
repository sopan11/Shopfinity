from django.db import models
from django.contrib.auth.models import User
from ecommerceapp.models import Product

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart: {self.user.username} - {self.product.product_name}"

    def total_price(self):
        return self.product.price * self.quantity
