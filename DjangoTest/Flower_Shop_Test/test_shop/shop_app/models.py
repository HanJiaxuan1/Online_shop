# Create your models here.
from django.db import models
import smtplib
import django.utils.timezone as timezone

# Create your models here.
from django.conf import settings


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
    product_desc = models.TextField()
    category = models.CharField(max_length=255)
    sub_category = models.CharField(max_length=255)
    price = models.IntegerField()
    publish_date = models.DateField()
    product_image = models.ImageField(upload_to='static/product')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f" Product: {self.product_id} - {self.product_name}"


class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    number = models.IntegerField()

    def __str__(self):
        return f" Cart: {self.cart_id} - {self.user} - {self.product}"


class Order(models.Model):
    STATUS_CHOICES = (
        ('unpaid', 'UNPAID'),
        ('paid', 'PAID'),
        ('shipped', 'SHIPPED'),
        ('delivered', 'DELIVERED'),
        ('received', 'RECEIVED'),
    )
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_list = models.CharField(max_length=255,)
    date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='unpaid')

    def __str__(self):
        return f" Order: {self.order_id} - {self.user} - {self.order_list}"
