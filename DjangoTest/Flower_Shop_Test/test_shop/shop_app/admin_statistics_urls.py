from django.conf.urls import url
from django.urls import path

from . import views, admin_views

app_name = 'shop_app_statistics'

urlpatterns = [
    path('', admin_views.statistics, name='statistics'),
]