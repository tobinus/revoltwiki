from django.test import TestCase

from .models import Member, Article, ArticleVersion, Category


class MemberTestCase(TestCase):
    def setUp(self):
        Member.objects.create(username='thedude',
                              email='the_dude@outlook.com',
                              password='whiterussian',
                              first_name='The',
                              last_name='Dude',
                              is_staff=False,
                              is_active=True)

    def test_short_name(self):
        """Users has a short name, equal to their first name"""

        thedude = Member.objects.get(username='thedude')

        self.assertEqual(thedude.get_short_name(), 'The')

    def test_full_name(self):
        """Users has a full name, equal to the first and last name"""

        thedude = Member.objects.get(username='thedude')

        self.assertEqual(thedude.get_full_name(), 'The Dude')

    def test_contributions_by_article(self):
        """When a user makes an article version, the parent article should appear once under contributions_by_article"""

        thedude = Member.objects.get(username='thedude')

        uncategorized = Category.objects.create(title='Uncategorized')

        caucasian = Article.objects.create(
            title='How to make an exquisite Caucasian',
            created_by=thedude,
            category=uncategorized)

        bowling = Article.objects.create(
            title='Bowling as a lifestyle; A guide to a better life.',
            created_by=thedude,
            category=uncategorized)

        self.assertListEqual(thedude.contributions_by_article(), [])

        ArticleVersion.objects.create(
            content='3 ice cubs, 1 part Kahlua, 2 part Vodka, fill with cream',
            parent_article=caucasian,
            created_by=thedude)

        self.assertListEqual(thedude.contributions_by_article(), [caucasian])

        ArticleVersion.objects.create(
            content='Add 3 ice cubs, 1 part Kahlua, 2 part Vodka, fill with cream.',
            parent_article=caucasian,
            created_by=thedude)

        self.assertListEqual(thedude.contributions_by_article(), [caucasian])

        ArticleVersion.objects.create(
            content='Just throw the damn thing.',
            parent_article=bowling,
            created_by=thedude)

        self.assertListEqual(thedude.contributions_by_article(), [caucasian, bowling])

    def test_contributions_by_version(self):
        """When a user makes an article version, the article version should appear under contributions_by_version"""

        thedude = Member.objects.get(username='thedude')

        uncategorized = Category.objects.create(title='Uncategorized')

        caucasian = Article.objects.create(
            title='How to make an exquisite Caucasian',
            created_by=thedude,
            category=uncategorized)

        bowling = Article.objects.create(
            title='Bowling for dummies',
            created_by=thedude,
            category=uncategorized)

        self.assertSequenceEqual(thedude.contributions_by_version.all(), [])

        caucasian_ver1 = ArticleVersion.objects.create(
            content='3 ice cubs, 1 part Kahlua, 2 part Vodka, fill with cream',
            parent_article=caucasian,
            created_by=thedude)

        self.assertSequenceEqual(thedude.contributions_by_version.all(), [caucasian_ver1])

        bowling_ver1 = ArticleVersion.objects.create(
            content='Just throw the damn thing.',
            parent_article=bowling,
            created_by=thedude)

        self.assertSequenceEqual(thedude.contributions_by_version.all(), [caucasian_ver1, bowling_ver1])

        caucasian_ver2 = ArticleVersion.objects.create(
            content='Add 3 ice cubs, 1 part Kahlua, 2 part Vodka, fill with cream.',
            parent_article=caucasian,
            created_by=thedude)

        self.assertSequenceEqual(thedude.contributions_by_version.all(), [caucasian_ver1, bowling_ver1, caucasian_ver2])


class CategoryTestCase(TestCase):
    def test_slug(self):
        """A category should have a slug that is a URL friendly version of the name"""

        cocktails = Category.objects.create(title='Everyday cocktails')

        self.assertEqual(cocktails.slug(), 'everyday-cocktails')

    def test_articles(self):
        """A category should contain all articles that uses it"""

        cocktails = Category.objects.create(title='Everyday cocktails')

        self.assertSequenceEqual(cocktails.articles.all(), [])

        thedude = Member.objects.create(username='thedude',
                                        email='the_dude@outlook.com',
                                        password='whiterussian',
                                        first_name='The',
                                        last_name='Dude',
                                        is_staff=False,
                                        is_active=True)

        caucasian = Article.objects.create(
            title='How to make an exquisite Caucasian',
            created_by=thedude,
            category=cocktails)

        self.assertSequenceEqual(cocktails.articles.all(), [caucasian])

        caucasian.delete()

        self.assertSequenceEqual(cocktails.articles.all(), [])
