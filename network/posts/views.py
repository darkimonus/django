from django.shortcuts import render, redirect
from .models import Post, Like, Emoji, Report
from profiles.models import Profile
from django.db.models import Count, Q
from .forms import PostModelForm, TopicModelForm, CommentModelForm, ReportModelForm
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

@login_required
def post_comment_create_and_list_view(request):
    # Getting reactions counts
    qs = Post.objects.annotate(
        like_count=Count('like', filter=Q(like__value='Like')),
        funny_count=Count('like', filter=Q(like__value='Funny')),
        sad_count=Count('like', filter=Q(like__value='Sad')),
        dislike_count=Count('like', filter=Q(like__value='Dislike')),
        empty_count=Count('like', filter=Q(like__value='Empty'))
    ).order_by('-updated')[:10]
    # getting emoji images for reactions
    emojis = Emoji.objects.all()
    # Topic, Post and Comment forms initials
    t_form = TopicModelForm()
    p_form = PostModelForm()
    c_form = CommentModelForm()
    post_added = False
    topic_added = False

    profile = Profile.objects.get(user=request.user)

    if 'submit_t_form' in request.POST:
        print(request.POST)
        t_form = TopicModelForm(request.POST, request.FILES)
        if t_form.is_valid():
            t_instance = t_form.save(commit=False)
            t_instance.author = profile
            t_instance.save()
            t_form = TopicModelForm()
            topic_added = True

    if 'submit_p_form' in request.POST:
        p_form = PostModelForm(request.POST, request.FILES)
        if p_form.is_valid():
            p_instance = p_form.save(commit=False)
            p_instance.author = profile
            p_instance.save()
            p_form = PostModelForm()
            post_added = True

    if 'submit_c_form' in request.POST:
        c_form = CommentModelForm(request.POST)
        if c_form.is_valid():
            c_instance = c_form.save(commit=False)
            c_instance.user = profile
            c_instance.post = Post.objects.get(id=request.POST.get('post_id'))
            c_instance.save()
            c_form = CommentModelForm()

    context = {
        'qs': qs,
        'emojis': emojis,
        'profile': profile,
        'p_form': p_form,
        't_form': t_form,
        'c_form': c_form,
        'post_added': post_added,
        'topic_added': topic_added,
    }

    return render(request, 'posts/main.html', context)


@login_required
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
                # if reaction is not the same
                else:
                    like = Like.objects.get(user=profile, post_id=post_id)
                    like.value = reaction
                    post_obj.save()
                    like.save()
            # if reaction doesn't exist
            else:
                post_obj.liked.add(profile)
                created = Like.objects.create(user=profile, post_id=post_id)
                created.value = reaction
                post_obj.save()
                created.save()

    return redirect(request.META.get('HTTP_REFERER'))


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'posts/confirm_del.html'
    success_url = reverse_lazy('posts:post-main')

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        obj = Post.objects.get(pk=pk)
        if not obj.author.user == self.request.user:
            messages.warning(self.request, 'You need to '
                                           'be the author of'
                                           ' the post in order to delete it')
        return obj


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostModelForm
    template_name = 'posts/update.html'
    success_url = reverse_lazy('posts:post-main')

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        if form.instance.author == profile:
            return super().form_valid(form)
        else:
            form.add_error(None, 'You need to '
                                 'be the author of'
                                 ' the post in order to delete it')
            return super().form_invalid(form)


@login_required
def create_report_view(request, post_id):
    r_form = ReportModelForm()
    post = Post.objects.annotate(
        like_count=Count('like', filter=Q(like__value='Like')),
        funny_count=Count('like', filter=Q(like__value='Funny')),
        sad_count=Count('like', filter=Q(like__value='Sad')),
        dislike_count=Count('like', filter=Q(like__value='Dislike')),
        empty_count=Count('like', filter=Q(like__value='Empty'))
    ).get(id=post_id)
    emojis = Emoji.objects.all()
    profile = Profile.objects.get(user=request.user)

    if 'submit_r_form' in request.POST:
        r_form = ReportModelForm(request.POST)
        if r_form.is_valid():
            r_instance = r_form.save(commit=False)
            r_instance.user = profile
            r_instance.post = Post.objects.get(id=post_id)
            r_instance.save()
            return redirect('posts:post-main')

    context = {
        'r_form': r_form,
        'post': post,
        'emojis': emojis,
        'profile': profile,
    }
    return render(request, 'posts/report.html', context)


def admin_view(request):
    profile = Profile.objects.get(user=request.user)
    if not profile.admin:
        return redirect('posts:post-main')
    else:
        posts = Post.objects.annotate(
            report_count=Count('reports')
        ).filter(report_count__gt=0).annotate(
            like_count=Count('like', filter=Q(like__value='Like')),
            funny_count=Count('like', filter=Q(like__value='Funny')),
            sad_count=Count('like', filter=Q(like__value='Sad')),
            dislike_count=Count('like', filter=Q(like__value='Dislike')),
            empty_count=Count('like', filter=Q(like__value='Empty'))
        ).order_by('-updated')
        emojis = Emoji.objects.all()

        if 'submit_warning' in request.POST:
            print(request.POST.get('report_id'))
            report = Report.objects.get(id=request.POST.get('report_id'))
            report.reviewed = True
            report.warning = True
            report.save()
            return redirect('posts:post-main')

        if 'mark_reviewed' in request.POST:
            report = Report.objects.get(id=request.POST.get('report_id'))
            report.reviewed = True
            report.save()
            return redirect('posts:post-main')

        if 'block_user' in request.POST:
            pass

        context = {
            'posts': posts,
            'emojis': emojis,
        }
        return render(request, 'posts/admin.html', context)
