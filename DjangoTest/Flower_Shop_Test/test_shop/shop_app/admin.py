from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Product, User, Order, Contact

admin.site.register(Product)
admin.site.register(User)
admin.site.register(Order)
admin.site.register(Contact)
