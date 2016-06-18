import graphene
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from data_models.models import Article, ArticleVersion, Category


# Types

class ArticleType(graphene.ObjectType):
    """
    Article description
    """
    name = 'Article'

    id = graphene.Int()
    title = graphene.String()
    slug = graphene.String()
    deleted = graphene.Boolean()
    created_at = graphene.String()
    updated_at = graphene.String()
    created_by = graphene.Field('UserType')
    category = graphene.Field('CategoryType')
    last_edited_by = graphene.Field('UserType')
    versions = graphene.List('ArticleVersionType')
    current_version = graphene.Field('UserType')
    authors = graphene.List('UserType')

    @staticmethod
    def resolve_created_by(article, args, info):
        return article.created_by

    @staticmethod
    def resolve_category(article, args, info):
        return article.category

    @staticmethod
    def resolve_last_edited_by(article, args, info):
        return article.last_edited_by()

    @staticmethod
    def resolve_versions(article, args, info):
        return article.versions.all()

    @staticmethod
    def resolve_current_version(article, args, info):
        return article.current_version

    @staticmethod
    def resolve_authors(article, args, info):
        return article.authors()

    @staticmethod
    def resolve_slug(article, args, info):
        return article.slug()


class ArticleVersionType(graphene.ObjectType):
    """
    Article version description
    """
    name = 'Article Version'

    id = graphene.Int()
    content = graphene.String()
    created_at = graphene.String()
    created_by = graphene.Field('UserType')
    parent_article = graphene.Field('ArticleType')

    @staticmethod
    def resolve_created_by(article_version, args, info):
        return article_version.created_by

    @staticmethod
    def resolve_parent_article(article_version, args, info):
        return article_version.parent_article


class CategoryType(graphene.ObjectType):
    """
    Category description
    """
    name = 'Category'

    id = graphene.Int()
    title = graphene.String()
    slug = graphene.String()
    articles = graphene.List('ArticleType')

    @staticmethod
    def resolve_articles(category, args, info):
        return category.articles.all()

    @staticmethod
    def resolve_slug(category, args, info):
        return category.slug()


class UserType(graphene.ObjectType):
    """
    User description
    """
    name = 'User'

    id = graphene.Int()
    username = graphene.String()
    email = graphene.String()
    contributions_by_version = graphene.List(ArticleVersionType)
    contributions_by_article = graphene.List(ArticleType)

    @staticmethod
    def resolve_contributions_by_article(user, args, info):
        return list(set([version.parent_article for version in user.contributions.all()]))

    @staticmethod
    def resolve_contributions_by_version(user, args, info):
        return user.contributions.all()


# Query

class Query(graphene.ObjectType):
    """
    Wiki query description
    """
    name = 'Query'

    category = graphene.Field(
        CategoryType,
        id=graphene.Int()
    )

    all_categories = graphene.List(
        CategoryType
    )

    article = graphene.Field(
        ArticleType,
        id=graphene.Int()
    )

    all_articles = graphene.List(
        ArticleType
    )

    article_version = graphene.Field(
        ArticleVersionType,
        id=graphene.Int()
    )

    all_article_version = graphene.List(
        ArticleVersionType
    )

    user = graphene.Field(
        UserType,
        id=graphene.Int()
    )

    all_users = graphene.List(
        UserType
    )

    @staticmethod
    def resolve_category(root, args, info):
        id = args.get('id')
        return Category.objects.get(pk=id)

    @staticmethod
    def resolve_all_categories(root, args, info):
        return Category.objects.all()

    @staticmethod
    def resolve_article(root, args, info):
        id = args.get('id')
        return Article.objects.get(pk=id)

    @staticmethod
    def resolve_all_articles(root, args, info):
        return Article.objects.all()

    @staticmethod
    def resolve_article_version(root, args, info):
        id = args.get('id')
        return ArticleVersion.objects.get(pk=id)

    @staticmethod
    def resolve_all_article_versions(root, args, info):
        return ArticleVersion.objects.all()

    @staticmethod
    def resolve_all_users(root, args, info):
        return User.objects.all()

    @staticmethod
    def resolve_user(root, args, info):
        id = args.get('id')
        return User.objects.get(pk=id)


# Mutations

class CreateCategory(graphene.Mutation):
    class Input:
        title = graphene.String()

    ok = graphene.Boolean()
    message = graphene.String()
    category = graphene.Field('CategoryType')

    @classmethod
    def mutate(cls, instance, args, info):
        title = args.get('title')
        ok = True
        message = ''
        try:
            # Må sjekke om brukeren er logget inn, og så må vi få tak i brukerobjektet
            # Jeg tror vi kan bruke @with_context-dekoratøren, men jeg fikk det ikke til
            category = Category(title=title)
            category.clean_fields()
            category.save()
        except ValidationError as error:
            category = None
            ok = False
            message = str(error)
        return CreateCategory(category=category, ok=ok, message=message)


class CreateUser(graphene.Mutation):
    class Input:
        username = graphene.String()
        password = graphene.String()
        email = graphene.String()

    ok = graphene.Boolean()
    message = graphene.String()
    user = graphene.Field('UserType')

    @classmethod
    def mutate(cls, instance, args, info):
        username = args.get('username')
        password = args.get('password')
        email = args.get('email')
        ok = True
        message = ''
        try:
            # Må sjekke om brukeren er logget inn, og så må vi få tak i brukerobjektet
            # Jeg tror vi kan bruke @with_context-dekoratøren, men jeg fikk det ikke til
            user = User(username=username, password=password, email=email)
            user.clean_fields()
            user.save()
        except ValidationError as error:
            user = None
            ok = False
            message = str(error)
        return CreateUser(user=user, ok=ok, message=message)


class CreateArticle(graphene.Mutation):
    class Input:
        title = graphene.String()
        category_id = graphene.Int()

    ok = graphene.Boolean()
    message = graphene.String()
    article = graphene.Field('ArticleType')

    @classmethod
    def mutate(cls, instance, args, info):
        title = args.get('title')
        category_id = args.get('category_id')
        ok = True
        message = ''
        try:
            # Må sjekke om brukeren er logget inn, og så må vi få tak i brukerobjektet
            # Jeg tror vi kan bruke @with_context-dekoratøren, men jeg fikk det ikke til
            category = Category.objects.get(pk=category_id)
            article = Article(title=title, category=category)
            article.clean_fields()
            article.save()
        except ValidationError as error:
            ok = False
            message = str(error)
            article = None
        except ObjectDoesNotExist as error:
            ok = False
            message = str(error)
            article = None
        return CreateArticle(article=article, ok=ok, message=message)


class CreateArticleVersion(graphene.Mutation):
    class Input:
        content = graphene.String()
        parent_article_id = graphene.Int()

    ok = graphene.Boolean()
    message = graphene.String()
    article_version = graphene.Field('ArticleVersionType')

    @classmethod
    def mutate(cls, instance, args, info):
        content = args.get('content')
        parent_article_id = args.get('parent_article_id')
        ok = True
        message = ''
        try:
            # Må sjekke om brukeren er logget inn, og så må vi få tak i brukerobjektet
            # Jeg tror vi kan bruke @with_context-dekoratøren, men jeg fikk det ikke til
            parent_article = ArticleVersion.objects.get(pk=parent_article_id)
            article_version = ArticleVersion(content=content, parent_article=parent_article)
            article_version.clean_fields()
            article_version.save()
        except ValidationError as error:
            ok = False
            message = str(error)
            article_version = None
        except ObjectDoesNotExist as error:
            ok = False
            message = str(error)
            article_version = None
        return CreateArticleVersion(article_version=article_version, ok=ok, message=message)

# Mutation


class Mutation(graphene.ObjectType):
    create_category = graphene.Field(CreateCategory)
    create_user = graphene.Field(CreateUser)
    create_article = graphene.Field(CreateArticle)
    create_article_version = graphene.Field(CreateArticleVersion)


schema = graphene.Schema(name='Wiki GraphQL Schema')
schema.query = Query
# schema.mutation = Mutation
