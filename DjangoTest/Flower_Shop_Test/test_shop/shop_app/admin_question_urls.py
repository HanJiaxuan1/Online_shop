from django.conf.urls import url
from django.urls import path

from . import views, admin_views

app_name = 'admin_question'

urlpatterns = [
    path('', admin_views.question, name='question'),
    path('<int:question_id>/', admin_views.question_detail, name='question_detail'),
    path('<int:question_id>/a_message/', admin_views.admin_message, name='adminNewMessage'),
]