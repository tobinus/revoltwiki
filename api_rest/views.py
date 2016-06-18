from django.contrib.auth.models import User
from rest_framework import viewsets

from api_rest.serializers import UserSerializer, ArticleSerializer, ArticleVersionSerializer, CategorySerializer
from data_models.models import Article, ArticleVersion, Category


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


class ArticleVersionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = ArticleVersion.objects.all().order_by('-created_at')
    serializer_class = ArticleVersionSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Category.objects.all().order_by('-title')
    serializer_class = CategorySerializer
