from django.conf.urls import url, include

from rest_framework import routers

from .views import MemberViewSet, CategoryViewSet, ArticleViewSet, ArticleVersionViewSet

rest_router = routers.DefaultRouter()
rest_router.register(r'members', MemberViewSet)
rest_router.register(r'articles', ArticleViewSet)
rest_router.register(r'article_versions', ArticleVersionViewSet)
rest_router.register(r'categories', CategoryViewSet)

urlpatterns = [
    url(r'^', include(rest_router.urls)),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework'))
]
