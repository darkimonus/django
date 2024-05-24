from django.contrib import admin
from .models import Post, Topic, Like, Comment, Emoji

admin.site.register(Post)
admin.site.register(Topic)
admin.site.register(Comment)
admin.site.register(Like)


@admin.register(Emoji)
class EmojiAdmin(admin.ModelAdmin):
    list_display = ('name', 'image',)