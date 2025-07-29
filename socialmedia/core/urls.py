from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('post/create/', views.create_post, name='create_post'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/comment/', views.comment_post, name='comment_post'),
    path('profile/edit/', views.edit_profile, name='edit_profile'), 
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('admin/post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('admin/comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('admin/user/<int:user_id>/delete/', views.delete_user, name='delete_user'),
    path('like/<int:post_id>/', views.like_post, name='like-post'),
    path('search/', views.search_users, name='search-users'),
    path("load-posts/", views.load_posts, name="load-posts"),
    path('follow/<str:username>/', views.follow_toggle, name='follow_toggle'),
    path('follow/', views.follow_user, name='follow_user')
]