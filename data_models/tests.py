from django.test import TestCase

from .models import Member, Article, ArticleVersion, Category


class MemberTestCase(TestCase):
    def setUp(self):
        self.dylan = Member.objects.create(username='dylan41',
                                           password='ihatewar',
                                           email='bob.dylan@gmail.com',
                                           first_name='Robert Allen',
                                           last_name='Zimmerman',
                                           is_staff=False,
                                           is_active=True)

        self.thedude = Member.objects.create(username='thedude',
                                             email='the_dude@outlook.com',
                                             password='whiterussian',
                                             first_name='The',
                                             last_name='Dude',
                                             is_staff=False,
                                             is_active=False)

        self.linus = Member.objects.create(username='linus',
                                           email='torvalds@linuxfoundation.org',
                                           password='l3n12ekXun1l',
                                           first_name='Linus Benedict',
                                           last_name='Torvalds',
                                           is_staff=True,
                                           is_active=True,
                                           is_superuser=True)

        self.uncategorized = Category.objects.create(title='Uncategorized')

        self.rollingstone = Article.objects.create(
            title='Rolling stone, it\'t is all about technique and precision',
            created_by=self.dylan,
            category=self.uncategorized)
        self.rollingstone_ver1 = ArticleVersion.objects.create(
            content='Try to let it blow in the wind.',
            parent_article=self.rollingstone,
            created_by=self.dylan)
        self.rollingstone_ver2 = ArticleVersion.objects.create(
            content='Just throw the damn thing.',
            parent_article=self.rollingstone,
            created_by=self.thedude)

        self.caucasian = Article.objects.create(
            title='How to make an exquisite Caucasian',
            created_by=self.thedude,
            category=self.uncategorized)
        self.caucasian_ver1 = ArticleVersion.objects.create(
            content='3 ice cubs, 1 part Kahlua, 2 part Vodka, fill with cream',
            parent_article=self.caucasian,
            created_by=self.thedude)
        self.caucasian_ver2 = ArticleVersion.objects.create(
            content='Add 3 ice cubs, 1 part Kahlua, 2 part Vodka, fill with cream.',
            parent_article=self.caucasian,
            created_by=self.thedude)

        self.kernelpatching = Article.objects.create(
            title='Patching the Linux kernel for dummies',
            created_by=self.linus,
            category=self.uncategorized)
        self.kernelpatching_ver1 = ArticleVersion.objects.create(
            content='Learn C, and then read the [documentation](https://www.kernel.org/doc/Documentation/).',
            parent_article=self.kernelpatching,
            created_by=self.linus)
        self.kernelpatching_ver2 = ArticleVersion.objects.create(
            content='Learn C, and then read the [documentation](https://www.kernel.org/doc/Documentation/). Good luck!',
            parent_article=self.kernelpatching,
            created_by=self.linus)

    def test_short_name(self):
        """Users has a short name, equal to their first name"""

        self.assertEqual(self.dylan.get_short_name(), 'Robert Allen')
        self.assertEqual(self.thedude.get_short_name(), 'The')
        self.assertEqual(self.linus.get_short_name(), 'Linus Benedict')

    def test_full_name(self):
        """Users has a full name, equal to the first and last name"""

        self.assertEqual(self.dylan.get_full_name(), 'Robert Allen Zimmerman')
        self.assertEqual(self.thedude.get_full_name(), 'The Dude')
        self.assertEqual(self.linus.get_full_name(), 'Linus Benedict Torvalds')

    def test_contributions_by_version(self):
        """Article versions created by the users should appear as contributions_by_version"""

        self.assertSequenceEqual(self.dylan.contributions_by_version.all(),
                                 [self.rollingstone_ver1])
        self.assertSequenceEqual(self.thedude.contributions_by_version.all(),
                                 [self.rollingstone_ver2, self.caucasian_ver1, self.caucasian_ver2])
        self.assertSequenceEqual(self.linus.contributions_by_version.all(),
                                 [self.kernelpatching_ver1, self.kernelpatching_ver2])

    def test_contributions_by_article(self):
        """Articles contributed to should appear as contributions_by_article"""

        self.assertListEqual(self.dylan.contributions_by_article(),
                             [self.rollingstone])
        self.assertListEqual(self.thedude.contributions_by_article(),
                             [self.rollingstone, self.caucasian])
        self.assertListEqual(self.linus.contributions_by_article(),
                             [self.kernelpatching])
