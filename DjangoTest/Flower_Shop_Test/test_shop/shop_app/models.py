# Create your models here.
from django.db import models
import smtplib
import django.utils.timezone as timezone

# Create your models here.
from django.conf import settings


class AdminProductInfo:
    product_obj = 'obj'
    product_num = 'num'

    def __init__(self, obj, num):
        self.product_num = num
        self.product_obj = obj


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
    product_desc = models.TextField()
    type = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    price = models.IntegerField()
    inventory = models.IntegerField(default=50)
    publish_date = models.DateField()
    product_image = models.ImageField(upload_to='media/static/product')
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
    order_list = models.CharField(max_length=255, )
    date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='unpaid')

    def __str__(self):
        return f" Order: {self.order_id} - {self.user} - {self.order_list}"

    def admin_retrieve_order(self):

        info = self.order_list
        product_details = info.split(';')

        p_list = ""
        for detail in product_details:
            if detail != '':
                product_obj = Product.objects.get(pk=int(detail.split(':')[0]))
                product_num = detail.split(':')[1]
                str_p_id = str(product_obj.product_id)
                str_p_name = product_obj.product_name

                p_list = p_list + "    |Id: " + str_p_id + "|    |Name: " + str_p_name + "|    |Number: " + product_num + "|\n"

        return p_list


class QuestionAnswer(models.Model):
    STATUS_CHOICES = (
        ('unread', 'UNREAD'),
        ('viewed', 'VIEWED'),
        ('answered', 'ANSWERED'),
        ('solved', 'SOLVED'),
    )
    SATISFACTION_CHOICE = (
        ('disappointed', 0),
        ('not really satisfied', 1),
        ('okay', 2),
        ('satisfied', 3),
        ('very satisfied', 4),
    )
    TYPE_CHOICE = (
        ('questions', 'QUESTION' ),
        ('trace', 'TRACE'),
        ('answer', 'ANSWER'),
    )
    qa_id = models.AutoField(primary_key=True)
    poster = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=1024, )
    date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='unread')
    satisfaction = models.IntegerField(choices=SATISFACTION_CHOICE, default='very satisfied')
    type = models.CharField(max_length=255, choices=TYPE_CHOICE, default='questions')

    def __str__(self):
        return f" QuestionAnswer: {self.qa_id} - {self.poster} - {self.content}"
