from django.contrib import admin
from .models import Product, Order, Staff, Customer


# Register your models here.
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Staff)
admin.site.register(Customer)
