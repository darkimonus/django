from django import forms
from .models import Topic, Post, Comment


class TopicModelForm(forms.ModelForm):
    name = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}))

    class Meta:
        model = Topic
        fields = ('name', 'image')


class PostModelForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}))

    class Meta:
        model = Post
        fields = ('content', 'image', 'topics')


class CommentModelForm(forms.ModelForm):
    body = forms.CharField(label='', widget=forms.TextInput(attrs=
                                                  {'placeholder': 'Comment..'}))

    class Meta:
        model = Comment
        fields = ('body',)
