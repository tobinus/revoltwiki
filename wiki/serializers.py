from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Article, ArticleVersion, Category


class ArticleVersionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ArticleVersion
        fields = ('id', 'content', 'parent_article', 'created_at', 'created_by')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    contributions = ArticleVersionSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'contributions')


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    authors = UserSerializer(many=True, read_only=True)
    last_edited_by = UserSerializer(read_only=True)

    class Meta:
        model = Article
        fields = ('id', 'title', 'category', 'current_version', 'deleted', 'created_at', 'updated_at', 'created_by',
                  'versions', 'authors', 'last_edited_by')


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title')
