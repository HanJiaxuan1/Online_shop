from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'shop_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:product_id>/', views.product, name='detail'),
    path('profile/', views.profile, name='profile'),
    path('cart/', views.cart, name='cart'),
    path('favorites/', views.favorites, name='favorites'),
    path('service/', views.service, name='service'),
    path('about_us/', views.about_us, name='about_us'),
    path('delete/', views.delete, name='delete'),
    path('delete_favorite/', views.delete_favorite, name='delete_favorite'),
    path('change_profile/', views.change_profile, name='change_profile'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('add_to_favorite/', views.add_to_favorite, name='add_to_favorite'),
    path('add_address/', views.add_address, name='add_address'),
    path('changenumber/', views.changenumber, name='changenumber'),
    path('commitorder/', views.addToOrder, name='addToOrder'),
    path('<int:order_id>/order/', views.order, name='order'),
    # path('<int:order_id>/payOrder/', views.payOrder, name='payOrder'),
    path('history_order/', views.history_order, name='history_order'),
    path('add_order/', views.add_order, name='add_order'),
    path('<int:question_id>/communication/', views.communication, name='communication'),
    path('<int:product_id>/tempOrder', views.orderNow, name='order_now'),
    path('question_create/', views.createQuestion, name='createQuestion'),
    path('<int:question_id>/message/', views.userMessage, name='newMessage'),
    path('address/', views.address, name='address'),
    path('classifier/', views.classifier, name='classifier'),
    path('prediction/', views.prediction, name='prediction'),
    path('result/', views.result, name='result'),
    path('DIY/', views.DIY, name='DIY')
]