from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Article, Content, Category


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'title', 'category', 'current_content', 'deleted', 'created_at', 'updated_at', 'created_by')


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title')


class ContentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Content
        fields = ('id', 'content', 'parent_article', 'created_at', 'created_by')
