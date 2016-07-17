from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.utils.deconstruct import deconstructible
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from django.core.exceptions import FieldError

from diff_match_patch import diff_match_patch


class MemberManager(BaseUserManager):
    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not username:
            raise ValueError('The given username must be set')
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        is_active = extra_fields.pop('is_active', True)
        user = self.model(username=username, email=email, is_staff=is_staff, is_active=is_active,
                          is_superuser=is_superuser, last_login=now, date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        is_staff = extra_fields.pop('is_staff', False)
        return self._create_user(username, email, password, is_staff, False, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        return self._create_user(username, email, password, True, True, **extra_fields)


class AbstractMember(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), max_length=40, unique=True)
    email = models.EmailField(_('email address'), max_length=254, unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as active. '
                                                'Deselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = MemberManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('member')
        verbose_name_plural = _('members')
        abstract = True

    def get_short_name(self):
        return '{first_name}'.format(first_name=self.first_name)

    def get_full_name(self):
        return '{first_name} {last_name}'.format(first_name=self.first_name, last_name=self.last_name)

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Member(AbstractMember):
    class Meta(AbstractMember.Meta):
        swappable = 'AUTH_USER_MODEL'

    def full_name(self):
        return self.get_full_name()

    def short_name(self):
        return self.get_short_name()

    def contributions_by_article(self):
        return list(set([version.parent_article for version in self.contributions_by_version.all()]))


@deconstructible
class Category(models.Model):
    title = models.CharField(max_length=128, unique=True)

    def slug(self):
        return slugify(self.title, allow_unicode=True)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return str(self.__unicode__())


class ArticleVersion(models.Model):
    content = models.TextField()
    parent_article = models.ForeignKey('Article', related_name='versions', related_query_name='version')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Member, related_name='contributions_by_version',
                                   related_query_name='version_contribution')

    def access(self):
        return self.parent_article.access

    def diff(self):
        try:
            previous_article_version = ArticleVersion.objects.filter(created_at__lt=self.created_at).order_by('-created_at')[0]
            diff = diff_match_patch()
            d = diff.diff_main(previous_article_version.content, self.content)
            diff.diff_cleanupSemantic(d)
            return [{'type': t, 'text': txt} for (t, txt) in d]
        except IndexError:
            return [{'type': 1, 'text': self.content}]

    # Sets the new article version as the current version of the parent article
    def save(self, *args, **kwargs):
        super(ArticleVersion, self).save(*args, **kwargs)
        self.parent_article.current_version = self
        self.parent_article.save()

    def __unicode__(self):
        return 'Versjon: {id}'.format(id=self.id)

    def __str__(self):
        return str(self.__unicode__())


class Article(models.Model):
    title = models.CharField(max_length=128, unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, related_name='articles',
                                 related_query_name='article', default=None)

    def allowed_versions(self):
        return {'parent_article': self.pk}

    current_version = models.ForeignKey(ArticleVersion, blank=True, null=True, default=None)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(Member, on_delete=models.PROTECT, related_name='+')

    class ACCESS:
        ALL = 0b1 << 0
        STAFF = 0b1 << 1
        SUPERUSER = 0b1 << 2

    ACCESS_CHOICES = (
        (ACCESS.ALL, _('All')),
        (ACCESS.STAFF, _('Staff')),
        (ACCESS.SUPERUSER, _('Superuser')),
        (ACCESS.STAFF | ACCESS.SUPERUSER, _('Staff or superuser'))
    )

    access = models.IntegerField(choices=ACCESS_CHOICES, default=ACCESS.ALL)

    def authors(self):
        return list(set([version.created_by for version in ArticleVersion.objects.filter(parent_article__id=self.id)]))

    def last_edited_by(self):
        try:
            return self.current_version.created_by
        except AttributeError:
            return None

    def slug(self):
        return slugify(self.title, allow_unicode=True)

    # Ensure that a article never has a 'current_version' that does not belong to that article
    def save(self, *args, **kwargs):
        if self.current_version:
            if self.pk != self.current_version.parent_article.pk:
                raise AttributeError(_('Cannot only assign versions that belongs to this article as current_version'))
        super(Article, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return str(self.__unicode__())
