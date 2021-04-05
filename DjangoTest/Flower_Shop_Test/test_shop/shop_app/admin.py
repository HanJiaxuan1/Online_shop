from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Product, Cart, Order

admin.site.register(Product)

admin.site.register(Cart)

admin.site.register(Order)

