from django.urls import path
from .views import (
    profile_view,
    invites_received_view,
    ProfileListView,
    invite_profiles_list_view,
    send_invitation,
    remove_from_friends,
    accept_invite,
    reject_invite,
    ProfileDetailView,
    SearchByPhotoView,
)

app_name = 'profiles'

urlpatterns = [
    path('', ProfileListView.as_view(), name='all-profiles-view'),
    path('myprofile', profile_view, name='my-profile-view'),
    path('my-invites/', invites_received_view, name='my-invites-view'),
    path('to-invite/', invite_profiles_list_view, name='invite-profiles-view'),
    path('send-invite/', send_invitation, name='send-invite'),
    path('remove-friend/', remove_from_friends, name='remove-friend'),
    path('<slug>', ProfileDetailView.as_view(), name='profile-detail-view'),
    path('my-invites/accept/', accept_invite, name='accept-invite'),
    path('my-invites/reject/', reject_invite, name='reject-invite'),
    path('search-by-photo/', SearchByPhotoView.as_view(), name='search-by-photo'),
]
