from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Product, Cart, Order






class OrderAdmin(admin.ModelAdmin):
    fields = ('order_id', 'user',  'admin_retrieve_order', 'date', 'status',)
    readonly_fields = ('order_id', 'user',  'admin_retrieve_order', 'date',)


admin.site.register(Product)

admin.site.register(Cart)

admin.site.register(Order, OrderAdmin)
