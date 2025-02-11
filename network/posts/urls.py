from django.urls import path
from posts.views import (
    post_comment_create_and_list_view,
    react_post,
    PostDeleteView,
    PostUpdateView,
    create_report_view,
    admin_view,
)


app_name = 'posts'

urlpatterns = [
    path('', post_comment_create_and_list_view, name='post-main'),
    path('reacted/', react_post, name='react-post'),
    path('<pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('<pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('<int:post_id>/report', create_report_view, name='make_report'),
    path('admin/', admin_view, name='admin-view')
]
