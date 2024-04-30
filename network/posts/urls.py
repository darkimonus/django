from django.urls import path
from .views import post_comment_create_and_list_view, react_post

app_name = 'posts'

urlpatterns = [
    path('', post_comment_create_and_list_view, name='post-main'),
    path('reacted/', react_post, name='react-post'),
]



