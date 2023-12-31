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
    receiver = models.CharField(max_length=255, default="user")
    phone = models.IntegerField(default="1234567890")
    address = models.CharField(max_length=512, default="Beijing")

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


class Question(models.Model):
    STATUS_CHOICES1 = (
        ('unread', 'UNREAD'),
        ('read', 'READ'),
        ('answered', 'ANSWERED'),
    )
    STATUS_CHOICES2 = (
        ("quality", 'QUALITY'),
        ('delivery', 'DELIVERY'),
        ('service', 'SERVICE'),
        ('order', 'ORDER'),
        ('product', 'PRODUCT'),
    )
    question_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=255, )
    category = models.CharField(max_length=255, choices=STATUS_CHOICES2, default='quality')
    date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES1, default='unread')
    satisfaction = models.IntegerField(default="5")


class QuestionDetails(models.Model):
    STATUS_CHOICES = (
        ('user', 'USER'),
        ('staff', 'STAFF'),
    )
    detail_id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=255, )
    source = models.CharField(max_length=20, choices=STATUS_CHOICES, default='user')
    date = models.CharField(max_length=50, default=timezone.now)


class Favorite(models.Model):
    favorite_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f" Favorite: {self.favorite_id} - {self.user} - {self.product}"


class Profile(models.Model):
    profile_id = models.AutoField(primary_key=True)
    userinfo = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_id')
    phone = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='user', blank=True, default="user1.jpg")

    def __str__(self):
        return 'Profile for {}'.format(self.profile_id)


class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=500)
    set_default = models.BooleanField(default=False)
    category = models.CharField(max_length=50)

    def __str__(self):
        return 'Address for {}'.format(self.address_id)


class DefaultAddress(models.Model):
    default_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    default_address = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self):
        return 'Default address for {}'.format(self.user)


class EpidemicMode(models.Model):
    id = models.AutoField(primary_key=True)
    mode = models.BooleanField(default=False)


class ProductComment(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=1000)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)


class Statistics(models.Model):
    id = models.AutoField(primary_key=True)
    mode = models.BooleanField(default=False)
