from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializers import UserSerializer, ArticleSerializer, ContentSerializer, CategorySerializer
from .models import Article, Content, Category


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Article.objects.all().order_by('-updated_at')
    serializer_class = ArticleSerializer


class ContentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Content.objects.all().order_by('-created_at')
    serializer_class = ContentSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Category.objects.all().order_by('-title')
    serializer_class = CategorySerializer
