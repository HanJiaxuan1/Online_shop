from django.db import models

# Create your models here.
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='user/%Y/%m/%d', blank=True)

    def __str__(self):
        return 'Profile for user {}'.format('self.user.username')


class OrderInfo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    receiver = models.CharField(max_length=255)
    phone = models.IntegerField()
    address = models.CharField(max_length=512)

    def __str__(self):
        return 'OrderInfo for user {}'.format('self.user.username')
