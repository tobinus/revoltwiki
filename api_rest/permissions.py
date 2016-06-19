from rest_framework.permissions import BasePermission, SAFE_METHODS
from data_models.models import Article, ArticleVersion, Member, Category


class MemberPermissions(BasePermission):
    """
    Permissions that describes access rights to members
    """

    def has_permission(self, request, view):
        """
        Permissions to list view and creation
        """

        # Everyone can view
        if request.method in SAFE_METHODS:
            return True

        # Only superusers can create
        return request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        """
        Permissions to detail view, update and delete
        """

        # Expecting the obj to be a member
        if type(obj) is not Member:
            raise TypeError('Expected Member type, but got {type}'.format(type=type(obj)))

        # Everyone can view
        if request.method in SAFE_METHODS:
            return True

        # Superusers can edit everyone, and users can edit themselves
        return request.user.is_superuser or request.user == obj.owner


class CategoryPermissions(BasePermission):
    """
    Permissions that describes access rights to categories
    """

    def has_permission(self, request, view):
        """
        Permissions to list view and creation
        """

        # Everyone can view
        if request.method in SAFE_METHODS:
            return True

        # Only staff can create
        return request.user.is_authenticated() and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        """
        Permissions to detail view, update and delete
        """

        # Expecting obj to be a category
        if type(obj) is not Category:
            raise TypeError('Expected Category type, but got {type}'.format(type=type(obj)))

        # Everyone can view
        if request.method in SAFE_METHODS:
            return True

        # Only staff can update and delete
        return request.user.is_staff


class ArticlePermissions(BasePermission):
    """
    Permissions that describes access rights to articles
    """

    def has_permission(self, request, view):
        """
        Permissions to list view, update and creation
        """

        # Everyone can view
        if request.method in SAFE_METHODS:
            return True

        # Only authenticated users can update and create
        return request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        """
        Permissions to detail view and update
        """

        # Expecting the obj to be an article
        if type(obj) is not Article:
            raise TypeError('Expected Article type, but got {type}'.format(type=type(obj)))

        # Handle anonymous users
        if not request.user.is_authenticated():
            # Only view articles with access set to ALL
            return request.method in SAFE_METHODS and obj.access == Article.ACCESS.ALL

        # Access ALL
        if obj.access == Article.ACCESS.ALL:
            return True

        # Access STAFF
        if obj.access & Article.ACCESS.STAFF and request.user.is_staff:
            return True

        # Access SUPERUSER
        if obj.access & Article.ACCESS.SUPERUSER and request.user.is_staff:
            return True

        # Fail switch (superusers should always be granted everything)
        return request.user.is_superuser


class ArticleVersionPermissions(BasePermission):
    """
    Permissions that describes access rights to article versions
    """

    def has_permission(self, request, view):
        """
        Permissions to list view and creation
        """

        # Everyone can view
        if request.method in SAFE_METHODS:
            return True

        # Only authenticated users can create
        return request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        """
        Permissions to detail view
        """

        # Expecting the obj to be an article version
        if type(obj) is not ArticleVersion:
            raise TypeError('Expected ArticleVersion type, but got {type}'.format(type=type(obj)))

        # Handling anonymous users
        if not request.user.is_authenticated():
            # Only view article versions with access set to ALL
            return request.method in SAFE_METHODS and obj.access() == Article.ACCESS.ALL

        # Access ALL
        if obj.access() == Article.ACCESS.ALL:
            return True

        # Access STAFF
        if obj.access() & Article.ACCESS.STAFF and request.user.is_staff:
            return True
        # Access SUPERUSER
        if obj.access() & Article.ACCESS.SUPERUSER and request.user.is_superuser:
            return True

        # Fail switch (superusers should always be granted everything)
        return request.user.is_superuser
