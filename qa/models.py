from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from django.db import models

# Create your models here.


class ProfileManager(models.Manager):
    def top(self):
        return self.all().order_by('-rating')

    @staticmethod
    def has(login):
        exists = True
        try:
            User.objects.get(username=login)
        except User.DoesNotExist:
            exists = False
        return exists

    def get_profile(self, user):
        if user.is_anonymous():
            return None
        return self.get(user=user)

    def profile_str(self, username):
        user = get_object_or_404(User, username=username)
        return self.get_profile(user)



class Profile(models.Model):
    objects = ProfileManager()
    user = models.OneToOneField(User)
    about_me = models.TextField(max_length=2000, default="")
    avatar = models.ImageField(upload_to='avatar/', null=True, default='avatar/default-user-image.png')
    rating = models.IntegerField(default=0)
    questions_count = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class QuestionManager(models.Manager):
    def new(self):
        return self.all().order_by('-id')

    def popular(self):
        return self.all().order_by('-rating')


class Question(models.Model):
    objects = QuestionManager()
    title = models.CharField(max_length=255)
    text = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(Profile, related_name="question_author")
    likes = models.ManyToManyField(Profile, related_name="question_like", blank=True)
    dislikes = models.ManyToManyField(Profile, related_name='question_dislike', blank=True)
    count_answers = models.PositiveIntegerField(default=0)
    short_text = models.TextField(max_length=85, default="")

    class Meta:
        ordering = ('-added_at',)

    def get_tags(self):
        return self.tag_set.all()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('question', kwargs={'pk': self.pk})

    @staticmethod
    def cut_text(text):
        text = text[:80] + '...'
        return text


class Answer(models.Model):
    text = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Question, null=False)
    author = models.ForeignKey(Profile, related_name='answer_author', null=False)
    rating = models.IntegerField(default=0)
    likes = models.ManyToManyField(Profile, related_name="answer_likes", blank=True)
    dislikes = models.ManyToManyField(Profile, related_name="answer_dislikes", blank=True)

    def __str__(self):
        return self.text


class TagsManager(models.Manager):
    def top(self):
        return self.all().order_by('-counts')

    def add(self, tag_name, question):
        try:
            tag = self.get(name=tag_name)
        except Tag.DoesNotExist:
            tag = Tag(name=tag_name)
            tag.save()

        tag.counts += 1
        tag.questions.add(question)
        tag.save()
        return tag


class Tag(models.Model):
    objects = TagsManager()
    questions = models.ManyToManyField(Question, blank=True)
    name = models.CharField(max_length=50)
    counts = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
