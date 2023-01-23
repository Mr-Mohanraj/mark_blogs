from django.urls import path 
from . import views

app_name='blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<int:pk>/detail/', views.blog_detail, name="blog_detail"),
    path('blog//<int:pk>/delete/', views.blog_delete, name="blog_delete"),
    path('blog/<str:username>/add/', views.blog_add, name='blog_add'),
    path('blog/<int:pk>/edit/', views.blog_edit, name='blog_edit'),
    path('user/signup/', views.signup_user, name='signup'),
    path('user/login/', views.login_user, name='login'),
    path('user/<str:username>/logout/', views.logout_user, name='logout'),
    path('blog/<int:user_id>/blogs/', views.user_blog, name='user_blog'),
]
