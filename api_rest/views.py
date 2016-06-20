from django.db.models import Q

from rest_framework import viewsets, mixins, status
from rest_framework.viewsets import GenericViewSet
from rest_framework.serializers import ValidationError

from data_models.models import Article, ArticleVersion, Category, Member

from .serializers import MemberSerializer, ArticleSerializer, ArticleVersionSerializer, CategorySerializer
from .permissions import MemberPermissions, CategoryPermissions, ArticlePermissions, ArticleVersionPermissions


class MemberViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):
    """
    API endpoint that allows members to be viewed, created or edited.
    """
    queryset = Member.objects.all().order_by('-date_joined')
    serializer_class = MemberSerializer
    permission_classes = [MemberPermissions]


class ArticleViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    """
    API endpoint that allows articles to be viewed, created or edited.
    """
    serializer_class = ArticleSerializer
    permission_classes = [ArticlePermissions]
    queryset = Article.objects.all().order_by('-updated_at')

    # Sets 'created_by' to the current user and that the 'current_version' is null
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, current_version=None)

    # Ensures that the 'current_version' belongs to this article (a little hackish)
    def perform_update(self, serializer):
        try:
            serializer.save()
        except AttributeError as error:
            raise ValidationError({'current_version': [str(error)]})

    def get_queryset(self):
        if self.request.user.is_authenticated():

            # Superusers
            if self.request.user.is_superuser:
                return Article.objects.all().order_by('-updated_at')

            # Staff
            if self.request.user.is_superuser:
                return Article.objects.get(
                    Q(access=Article.ACCESS.ALL) |
                    Q(access=Article.ACCESS.STAFF)
                ).order_by('-updated_at')

        return Article.objects.filter(access=Article.ACCESS.ALL).order_by('-updated_at')


class ArticleVersionViewSet(mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.ListModelMixin,
                            GenericViewSet):
    """
    API endpoint that allows article versions to be viewed or created.
    """
    queryset = ArticleVersion.objects.all().order_by('-created_at')
    serializer_class = ArticleVersionSerializer
    permission_classes = [ArticleVersionPermissions]

    # Override the default create-method to force 'created_by' to be the current user
    # Sets 'created_by' to the current user and that the 'current_version' is null
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        if self.request.user.is_authenticated():

            # Superusers
            if self.request.user.is_superuser:
                return ArticleVersion.objects.all().order_by('-created_at')

            # Staff
            if self.request.user.is_superuser:
                return ArticleVersion.objects.get(
                    Q(parent_article__access=Article.ACCESS.ALL) |
                    Q(parent_article__access=Article.ACCESS.STAFF)
                ).order_by('-created_at')

        return ArticleVersion.objects.filter(parent_article__access=Article.ACCESS.ALL).order_by('-created_at')


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows categories to be viewed, created, edited or deleted.
    """
    queryset = Category.objects.all().order_by('-title')
    serializer_class = CategorySerializer
    permission_classes = [CategoryPermissions]
