from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'shop_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:product_id>/', views.product, name='detail'),
    path('profile/', views.profile, name='profile'),
    path('cart/', views.cart, name='cart'),
    path('service/', views.service, name='service'),
    path('about_us/', views.about_us, name='about_us'),
    path('delete/', views.delete, name='delete'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('changenumber/', views.changenumber, name='changenumber'),
    path('commitorder/', views.addToOrder, name='addToOrder'),
    path('<int:order_id>/order/', views.order, name='order'),
    # path('<int:order_id>/payOrder/', views.payOrder, name='payOrder'),
    path('add_order/', views.add_order, name='add_order'),
    path('communication/', views.communication, name='communication'),
]