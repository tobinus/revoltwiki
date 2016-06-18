from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.utils.text import slugify


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


class Category(models.Model):
    title = models.CharField(max_length=128)

    def slug(self):
        return slugify(self.title, allow_unicode=True)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.__unicode__()


class ArticleVersion(models.Model):
    content = models.TextField()
    parent_article = models.ForeignKey('Article', related_name='versions', related_query_name='version')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='contributions', related_query_name='contribution')

    def __unicode__(self):
        return '{title} @ {date} ({author})'.format(title=self.parent_article.title,
                                                    date=self.created_at,
                                                    author=self.created_by.username)

    def __str__(self):
        return self.__unicode__()


class Article(models.Model):
    title = models.CharField(max_length=128)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='articles',
                                 related_query_name='article')
    current_version = models.ForeignKey(ArticleVersion, blank=True, null=True, default=None)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user), related_name='+')

    def authors(self):
        return list(set([version.created_by for version in ArticleVersion.objects.filter(parent_article__id=self.id)]))

    def last_edited_by(self):
        try:
            return self.current_version.created_by
        except AttributeError:
            return None

    def slug(self):
        return slugify(self.title, allow_unicode=True)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.__unicode__()

