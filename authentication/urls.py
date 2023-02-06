from django.urls import path
from authentication import views
from authentication import follower_system

app_name = "auth"

urlpatterns = [
    path('user/signup/', views.signup_user, name='signup'),
    path('user/login/', views.login_user, name='login'),
    path('user/<str:username>/logout/', views.logout_user, name='logout'),
    path('password/<str:username>/change/',
         views.password_change, name='password_change'),
    # path('password/<str:username>/reset', views.password_reset, name="password_reset"),
    path('password/<str:username>/forgot/',
         views.password_forgot, name='password_forgot'),
    path('password/<str:token>/forgot/change/',
         views.forgot_password_change, name="password_forgot_change"),
    path('user/<str:token>/activation/',
         views.activation, name="user_activation"),
    path('user/<str:author>/add_follow/',follower_system.add_follower,name="add_follower"),
    path('user/<str:author>/remove_follow/', follower_system.remove_follower,name="remove_follower"),
#     path('user/<int:pk>/add_unfollow/', follower_system.add_following,name="add_following"),
#     path('user/<int:pk>/remove_unfollow/', follower_system.remove_following,name="remove_following"),
    path('user/all/', views.all_users, name="all_users"),
    # path('<int:pk>/share/', views.post_share, name="post_share"),
    path('profile/<int:pk>/view/', views.profile, name="profile"),
    path('profile/<int:pk>/follower/', follower_system.view_follower, name="follower_profile"),
    path('profile/<int:pk>/following/', follower_system.view_following, name="following_profile"),
    path('search/',views.search_user, name="search_user")
    # path('profile/<int:pk>/edit/', views.profile_edit,name="profile_edit"),
    # path('profile/<int:pk>/update/', views.profile_update, name="profile_update"),
    # path('profile/<int:pk>/share/', views.profile_share, nme="profile_share"),
    # path('profile/<int:pk>/dashboard/', views.profile_dash, name="profile_dash"),
    # path('/<str:username>/view/', views.profile_other,name="profile_view"),
    
]
