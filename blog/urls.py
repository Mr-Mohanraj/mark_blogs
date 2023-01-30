from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<int:pk>/detail/', views.blog_detail, name="blog_detail"),
    path('blog/<int:pk>/delete/', views.blog_delete, name="blog_delete"),
    path('blog/<str:username>/add/', views.blog_add, name='blog_add'),
    path('blog/<int:pk>/edit/', views.blog_edit, name='blog_edit'),
    path('user/signup/', views.signup_user, name='signup'),
    path('user/login/', views.login_user, name='login'),
    path('user/<str:username>/logout/', views.logout_user, name='logout'),
    path('blog/<int:user_id>/blogs/', views.user_blog, name='user_blog'),
    path('password/<str:username>/change/',
         views.password_change, name='password_change'),
    # path('password/<str:username>/reset', views.password_reset, name="password_reset"),
    path('password/<str:username>/forgot/',
         views.password_forgot, name='password_forgot'),
    path('password/<str:token>/forgot/change/',
         views.forgot_password_change, name="password_forgot_change"),
    path('user/<str:token>/activation/',
         views.activation, name="user_activation"),
    # path('<int:pk>/share/', views.post_share, name="post_share"),
    # path('profile/<int:pk>/view/', views.profile_view,name="profile"),
    # path('profile/<int:pk>/edit/', views.profile_edit,name="profile"),
    # path('profile/<int:pk>/update/', views.profile_update, name="profile_update"),
    # path('profile/<int:pk>/share/', views.profile_share, nme="profile_share"),
    # path('profile/<int:pk>/dashboard/', views.profile_dash, name="profile_dash"),
    # path('/<str:username>/view/', views.profile_other,name="profile_view"),
]

urlpatterns += staticfiles_urlpatterns();