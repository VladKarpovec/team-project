from django.contrib import admin
from .models import Thread, Post

# Register your models here.
@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')

    def author(self, obj):
        first_post = obj.posts.first()
        return obj.first_post.author if first_post else None


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('thread', 'author', 'like_count', 'created_at', 'updated_at')

    def like_count(self, obj):
        return obj.likes.count()
