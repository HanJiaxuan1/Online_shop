from django.conf.urls import url
from django.urls import path

from . import views, admin_views

app_name = 'shop_app_order'
urlpatterns = [
    path('', admin_views.order, name='order'),
]