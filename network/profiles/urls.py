from django.urls import path
from .views import profile_view

app_name = 'profiles'

urlpatterns = [
    path('myprofile', profile_view, name='my-profile-view')
]



