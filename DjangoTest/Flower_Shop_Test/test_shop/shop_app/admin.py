from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Product, Cart, Order, Question, QuestionDetails


admin.site.site_header = 'Bouquet Pickup Admin'

class OrderAdmin(admin.ModelAdmin):
    fields = ('order_id', 'user',  'admin_retrieve_order', 'date', 'status', 'receiver', 'phone', 'address')
    readonly_fields = ('order_id', 'user',  'admin_retrieve_order', 'date', 'receiver', 'phone', 'address')


admin.site.register(Product)

admin.site.register(Question)

admin.site.register(Order, OrderAdmin)
