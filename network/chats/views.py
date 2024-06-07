from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from profiles.models import Profile
from .utils import generate_chat_room_name


@login_required
def chat_main_view(request):
    profile = Profile.objects.get(user=request.user)
    friends = profile.get_friends_profiles()

    return render(request, 'chats/main.html', {'friends': friends})


@login_required
def private_chat_view(request, user_id):
    room_name = generate_chat_room_name(request.user.id, user_id)
    return render(request, 'chats/chatroom.html', {'room_name': room_name})
