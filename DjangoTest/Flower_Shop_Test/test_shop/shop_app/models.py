from django.db import models

# Create your models here.

from django.db import models
import smtplib


# Create your models here.

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


class User(models.Model):
    USER_STATUS = (
        ('normal', 'NORMAL'),
        ('vip', 'VIP'),
    )
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    address = models.TextField()
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)

    user_status = models.CharField(max_length=255, choices=USER_STATUS, default='active')

    def __str__(self):
        return f" User: {self.user_id} - {self.first_name}"


class Order(models.Model):
    STATUS_CHOICES = (
        ('active', 'ACTIVE'),
        ('shipped', 'SHIPPED'),
        ('deliver', 'DELIVER'),
    )
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    total_price = models.CharField(max_length=255, default="")
    date = models.CharField(max_length=255, default="")
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='active')
    ordered_item = models.TextField()

    def __str__(self):
        return f" Order: {self.order_id} - {self.user} - {self.ordered_item}"

class Contact(models.Model):
    contact_id  = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()

    def __str__(self):
        return f" Contact: {self.contact_id} - {self.user}"
