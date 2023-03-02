from django.urls import path
from user_profile import follower_system
from user_profile import views

app_name ="profile"

urlpatterns = [
    path('user/<str:author>/add_follow/',follower_system.add_follower,name="add_follower"),
    path('user/<str:author>/remove_follow/', follower_system.remove_follower,name="remove_follower"),
    path('user/all/', views.all_users, name="all_users"),
    path('profile/<int:pk>/view/', views.profile, name="profile"),
    path('profile/<int:pk>/follower/', follower_system.view_follower, name="follower_profile"),
    path('profile/<int:pk>/following/', follower_system.view_following, name="following_profile"),
    path('search/',views.search_user, name="search_user")
    
    # path('<int:pk>/share/', views.post_share, name="post_share"),
    # path('profile/<int:pk>/edit/', views.profile_edit,name="profile_edit"),
    # path('profile/<int:pk>/update/', views.profile_update, name="profile_update"),
    # path('profile/<int:pk>/share/', views.profile_share, nme="profile_share"),
    # path('profile/<int:pk>/dashboard/', views.profile_dash, name="profile_dash"),
    # path('/<str:username>/view/', views.profile_other,name="profile_view"),
]
