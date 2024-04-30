from django.shortcuts import render, redirect
from .models import Topic, Post, Like, Comment, Emoji
from profiles.models import Profile
from django.db.models import Count, Q

# Create your views here.


def post_comment_create_and_list_view(request):
    qs = Post.objects.annotate(
        like_count=Count('like', filter=Q(like__value='Like')),
        funny_count=Count('like', filter=Q(like__value='Funny')),
        sad_count=Count('like', filter=Q(like__value='Sad')),
        dislike_count=Count('like', filter=Q(like__value='Dislike')),
        empty_count=Count('like', filter=Q(like__value='Empty'))
    ).order_by('-updated')[:10]
    emojis = Emoji.objects.all()
    profile = Profile.objects.get(user=request.user)

    context = {
        'qs': qs,
        'emojis': emojis,
        'profile': profile,
    }

    return render(request, 'posts/main.html', context)


def react_post(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)
        profile = Profile.objects.get(user=user)
        reaction = request.POST.get('reaction')

        if reaction:
            # if reaction exists
            if profile in post_obj.liked.all():
                # if reaction is the same
                if Like.objects.get(user=profile, post=post_obj).value == reaction:
                    post_obj.liked.remove(profile)
                    like = Like.objects.get(user=profile, post=post_obj)
                    like.delete()
                    return redirect('posts:post-main')
                #if reaction is not the same
                else:
                    like = Like.objects.get(user=profile, post_id=post_id)
                    like.value = reaction
                    post_obj.save()
                    like.save()
            #if reaction doesn't exist
            else:
                post_obj.liked.add(profile)
                created = Like.objects.create(user=profile, post_id=post_id)
                created.value = reaction
                post_obj.save()
                created.save()

    return redirect('posts:post-main')
