from django.contrib import admin
from accounts.models import User
from posts.models import Post

# Register your models here.

admin.site.register(User)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "created"]
    list_filter = ["title", "created"]
