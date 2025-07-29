from django.contrib import admin
from django.contrib.auth.models import User
from .models import Post, Comment, Follow, Profile 


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'caption', 'created_at')
    search_fields = ('user__username', 'caption')
    list_filter = ('created_at',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post', 'text', 'created_at')
    search_fields = ('user__username', 'text')

class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'follower', 'following', 'followed_at')
    search_fields = ('follower__username', 'following__username')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')
    search_fields = ('user__username', 'bio')

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Profile, ProfileAdmin)