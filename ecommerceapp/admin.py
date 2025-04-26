from django.contrib import admin
from ecommerceapp.models import Contact, Product, Orders, OrderUpdate

# Register your models here.
admin.site.register(Contact)
admin.site.register(Product)
admin.site.register(OrderUpdate)
admin.site.register(Orders)

