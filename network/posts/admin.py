from django.contrib import admin
from .models import Post, Topic, Like, Comment, Emoji, Report

admin.site.register(Post)
admin.site.register(Topic)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Report)


@admin.register(Emoji)
class EmojiAdmin(admin.ModelAdmin):
    list_display = ('name', 'image',)
