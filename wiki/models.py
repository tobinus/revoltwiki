from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.utils.text import slugify


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


class Category(models.Model):
    title = models.CharField(max_length=128)

    def slug(self):
        return str(self)

    def __unicode__(self):
        return slugify(self.title, allow_unicode=True)


class Content(models.Model):
    content = models.TextField()
    article = models.ForeignKey('Article')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User)


class Article(models.Model):
    title = models.CharField(max_length=128)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    current_content = models.ForeignKey(Content)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user))

    def authors(self):
        return [content.created_by for content in Content.objects.filter(article=self)]

    def last_edited_by(self):
        return self.current_content.created_by

    def slug(self):
        return str(self)

    def __unicode__(self):
        return slugify(self.title, allow_unicode=True)

