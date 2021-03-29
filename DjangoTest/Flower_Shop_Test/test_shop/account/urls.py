from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'account'

urlpatterns = [
    # previous login view
    # path('login/', views.user_login, name='login'),
    path('mainpage/', views.mainpage, name='mainpage'),
    path('login/', auth_views.LoginView.as_view(
        template_name='user/login.html'
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='user/logged_out.html'
    ), name='logout'),

    path('edit/', views.edit, name='edit'),

    # change password urls
    path('password_change/',
         auth_views.PasswordChangeView.as_view(
            template_name='user/password_change_form.html',
            success_url='/account/password_change/done'
         ),
         name='password_change'),
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(
            template_name='user/password_change_done.html'
         ),
         name='password_change_done'),

    # reset password urls
    path('password_reset/',
         auth_views.PasswordResetView.as_view(
            template_name='user/password_reset_form.html',
            success_url='/account/password_reset/done'
         ),
         name='password_reset'),

    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(
            template_name='user/password_reset_done.html'
         ),
         name='password_reset_done'),

    path('password_reset_confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
            template_name='user/password_reset_confirm.html',
            success_url='/account/login'
         ),
         name='password_reset_confirm'),




    # path('reset/<uidb64>/<token>/',
    #      auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    #

    path('password_reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(
            template_name='user/password_reset_complete.html',
         ),
         name='password_reset_complete'),

    path('register/', views.register, name='register'),
]
