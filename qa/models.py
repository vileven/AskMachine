from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

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


class Profile(models.Model):
    objects = ProfileManager()
    user = models.OneToOneField(User)
    avatar = models.ImageField(upload_to='avatar/', null=True)
    rating = models.IntegerField(default=0)

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

    class Meta:
        ordering = ('-added_at',)

    def get_tags(self):
        return self.tag_set.all()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('question', kwargs={'pk': self.pk})


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

        tag.count += 1
        tag.questions.add(question)
        tag.save()
        return tag


class Tag(models.Model):
    objects = TagsManager()
    question = models.ManyToManyField(Question, blank=True)
    name = models.CharField(max_length=50)
    counts = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
