from django.urls import path
from . import views
from .feeds import LatestPostsFeed

app_name = 'blog'

urlpatterns = [
    # Post views
    path('', views.post_list, name='blog_list'),
    # path('', views.PostListView.as_view(), name='post_list'),
    path('tag/<slug:tag_slug>/',
         views.post_list, name='post_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<int:post>/',
         views.post_detail,
         name='blog_detail'),
    path('<int:post_id>/share/',
         views.post_share, name='post_share'),
    path('<int:post_id>/comment/',
         views.post_comment, name='post_comment'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path('search/', views.post_search, name='post_search'),
    path('<int:user_id>/blogs/', views.user_blog, name='user_blog'),
    path('<int:pk>/likes/', views.add_likes, name="likes"),
#     path('blog/', views.BlogList.as_view(), name='blog_list'),
#     path('blog/<int:pk>/detail/', views.blog_detail, name="blog_detail"),
    path('<int:pk>/delete/', views.blog_delete, name="blog_delete"),
    path('<str:username>/add/', views.blog_add, name='blog_add'),
    path('<int:pk>/edit/', views.blog_edit, name='blog_edit'),
    # path('search/', views.post_search, name='post_search'),
    path('<int:post_id>/comment/',
         views.post_comment, name='post_comment'),
    path('<int:post_id>/share/',
         views.post_share, name='post_share'),
]
