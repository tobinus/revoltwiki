from django.contrib.auth.models import User
from rest_framework import serializers

from data_models.models import Article, ArticleVersion, Category


class ArticleVersionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ArticleVersion
        fields = ('id', 'content', 'parent_article', 'created_at', 'created_by')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'contributions', 'password')
        extra_kwargs = {'password': {'write_only': True, 'style': {'input_type': 'password'}}}


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    authors = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='user-detail')
    last_edited_by = serializers.HyperlinkedRelatedField(read_only=True, view_name='user-detail')

    class Meta:
        model = Article
        fields = ('id', 'title', 'category', 'slug', 'current_version', 'deleted', 'created_at', 'updated_at',
                  'created_by', 'versions', 'authors', 'last_edited_by')
        extra_kwargs = {'versions': {'read_only': True}}


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title', 'slug', 'articles')
