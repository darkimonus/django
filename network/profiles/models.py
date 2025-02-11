from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.shortcuts import reverse

from profiles.utils import get_random_code
from profiles.choices import STATUS_CHOICES
from profiles.managers import ProfileManager, RelationshipManager


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    bio = models.TextField(
        default='-',
        max_length=300
    )
    email = models.CharField(max_length=30)
    first_name = models.CharField(
        max_length=30,
        blank=True
    )
    last_name = models.CharField(
        max_length=30,
        blank=True
    )
    country = models.CharField(max_length=30)
    avatar = models.ImageField(
        default='avatars/avatar.png',
        upload_to='avatars/'
    )
    friends = models.ManyToManyField(
        User,
        blank=True,
        related_name='friends'
    )
    slug = models.SlugField(
        unique=True,
        blank=True
    )
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    admin = models.BooleanField(default=False)

    objects = ProfileManager()

    def __str__(self):
        return f"{self.user.username}--{self.created.strftime('%d-%m-%Y')}"

    def get_absolute_url(self):
        return reverse('profiles:profile-detail-view', kwargs={'slug': self.slug})

    def get_friends(self):
        return self.friends.all()

    def get_friends_profiles(self):
        friends = self.get_friends()
        friends_profiles = []
        for obj in friends:
            friends_profiles.append(Profile.objects.get(user=obj))
        return friends_profiles

    def get_friends_no(self):
        return self.friends.all().count()

    def get_posts_no(self):
        return self.posts.all().count()

    def get_topics_no(self):
        return self.topics.all().count()

    def get_all_authors_posts(self):
        return self.posts.all()

    def get_likes_given_no(self):
        likes = self.like_set.all()
        total_liked = 0
        for item in likes:
            if item.value != 'Empty':
                total_liked += 1
        return total_liked

    def get_likes_received_no(self):
        posts = self.posts.all()
        total_liked = 0
        for item in posts:
            total_liked += item.liked.all().count()
        return total_liked

    __initial_first_name = None
    __initial_last_name = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__initial_first_name = self.first_name
        self.__initial_last_name = self.last_name

    def save(self, *args, **kwargs):
        ex = False
        to_slug = self.slug
        if (self.first_name != self.__initial_first_name
                or self.last_name != self.__initial_last_name or self.slug == ""):
            if self.first_name and self.last_name:
                to_slug = slugify(str(self.first_name) + " " + str(self.last_name))
                ex = Profile.objects.filter(slug=to_slug).exists()
                while ex:
                    to_slug = slugify(to_slug + " " + str(get_random_code()))
                    ex = Profile.objects.filter(slug=to_slug).exists()
            else:
                to_slug = str(self.user)
        self.slug = to_slug
        super().save(*args, **kwargs)


class Relationship(models.Model):
    sender = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='sender'
    )
    receiver = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='receiver'
    )
    status = models.CharField(
        max_length=8,
        choices=STATUS_CHOICES
    )
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = RelationshipManager()

    def __str__(self):
        return f'{self.sender}--{self.receiver}--{self.status}'
