from django.urls import path
from authentication import views
from user_profile import follower_system

app_name = "auth"

urlpatterns = [
    path('user/signup/', views.signup_user, name='signup'),
    path('user/login/', views.login_user, name='login'),
    path('user/<str:username>/logout/', views.logout_user, name='logout'),
    path('password/<str:username>/change/',
         views.password_change, name='password_change'),
    path('password/<str:username>/forgot/',
         views.password_forgot, name='password_forgot'),
    path('password/<str:token>/forgot/change/',
         views.forgot_password_change, name="password_forgot_change"),
    path('user/<str:token>/activation/',
         views.activation, name="user_activation"),
     path('activation/',views.activationPage, name="activation" ),
     path('activation/<str:username>/resend', views.resendActivation, name="resendA"),
]
