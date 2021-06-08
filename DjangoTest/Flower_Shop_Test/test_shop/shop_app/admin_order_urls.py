from django.conf.urls import url
from django.urls import path

from . import views, admin_views

app_name = 'admin_order'
urlpatterns = [
    path('', admin_views.order, name='order'),
    # path('/<int:order_id>/', admin_views.order_detail, name='order_detail'),
]