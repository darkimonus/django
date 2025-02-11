from django.db import models
from django.core.validators import FileExtensionValidator

from posts.choices import LIKE_CHOICES

from profiles.models import Profile


class Topic(models.Model):
    name = models.TextField(max_length=30)
    author = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='topics'
    )
    image = models.ImageField(
        upload_to="topics",
        validators=[
            FileExtensionValidator(['png', 'jpg', 'jpeg'])],
        blank=True
    )
    liked = models.ManyToManyField(
        Profile,
        blank=True,
        related_name='topic_likes'
    )

    def __str__(self):
        return str(self.name)


class Post(models.Model):
    content = models.TextField()
    image = models.ImageField(
        upload_to="posts",
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])],
        blank=True
    )
    liked = models.ManyToManyField(
        Profile,
        blank=True,
        related_name='post_likes'
    )
    topics = models.ManyToManyField(
        Topic,
        blank=True,
        related_name='post_topics'
    )
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='posts'
    )

    def __str__(self):
        if len(self.content) > 25:
            return f"{len(self.content)} symbols--{self.content[:20]}..--{self.created.strftime('%d-%m-%Y')}"
        else:
            return f"{self.content}--{self.created.strftime('%d-%m-%Y')}"

    def num_likes(self):
        return self.liked.all().count()

    def num_comments(self):
        return self.comment_set.all().count()

    class Meta:
        ordering = ('-created',)


class Comment(models.Model):
    user = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )
    body = models.TextField(max_length=300)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    liked = models.ManyToManyField(
        Profile,
        default=None,
        related_name='comment_likes'
    )

    def __str__(self):
        return str(self.pk)


class Like(models.Model):
    user = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )
    value = models.CharField(
        choices=LIKE_CHOICES,
        max_length=8
    )
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user}--{self.post}--{self.value}'


class Emoji(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True
    )
    image = models.ImageField(upload_to='emojis/')

    def __str__(self):
        return self.name


class Report(models.Model):
    user = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='reports'
    )
    text = models.TextField(max_length=300)
    negative = models.BooleanField(default=True)
    reviewed = models.BooleanField(default=False)
    warning = models.BooleanField(default=False)
