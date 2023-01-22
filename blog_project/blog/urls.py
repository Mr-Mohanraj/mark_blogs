from django.urls import path 
from . import views

app_name='blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('blogs/', views.blog_list, name='blog_list'),
    path('detail/<int:pk>/', views.blog_detail, name="blog_detail"),
    # path('update/<int:pk>/', views.blog_update, name="blog_update"),
    path('delete/<int:pk>/', views.blog_delete, name="blog_delete"),
    path('post/<str:username>/add/', views.blog_add, name='blog_add'),
    path('<int:pk>/edit', views.blog_edit, name='blog_edit'),
    path('user/signup/', views.signup_user, name='signup'),
    path('user/login/', views.login_user, name='login'),
    path('user/<str:username>/logout/', views.logout_user, name='logout'),
]
