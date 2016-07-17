from rest_framework import serializers

from data_models.models import Article, ArticleVersion, Category, Member


class ArticleVersionSerializer(serializers.HyperlinkedModelSerializer):
    diff = serializers.JSONField()

    class Meta:
        model = ArticleVersion
        fields = ('id', 'url', 'content', 'access', 'parent_article', 'created_at', 'created_by', 'diff')
        read_only_fields = ('id', 'url', 'access', 'created_at', 'created_by', 'diff')


class MemberSerializer(serializers.HyperlinkedModelSerializer):
    contributions_by_article = serializers.HyperlinkedRelatedField(many=True, read_only=True,
                                                                   view_name='article-detail')

    class Meta:
        model = Member
        fields = ('id', 'url', 'username', 'email', 'first_name', 'last_name', 'full_name', 'short_name', 'date_joined',
                  'is_staff', 'is_superuser', 'is_active', 'contributions_by_article', 'contributions_by_version',
                  'password')
        read_only_fields = ('id', 'url', 'full_name', 'short_name', 'date_joined', 'contributions_by_article',
                            'contributions_by_version')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {
                    'input_type': 'password'
                }
            },
        }


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    authors = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='member-detail')
    last_edited_by = serializers.HyperlinkedRelatedField(read_only=True, view_name='member-detail')

    class Meta:
        model = Article
        fields = ('id', 'url', 'title', 'category', 'slug', 'access', 'current_version', 'deleted', 'created_at',
                  'updated_at', 'created_by', 'versions', 'authors', 'last_edited_by')
        read_only_fields = ('id', 'url', 'slug', 'created_at', 'updated_at', 'created_by',
                            'versions', 'authors', 'last_edited_by')


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'url', 'title', 'slug', 'articles')
        read_only_fields = ('id', 'url', 'articles')
