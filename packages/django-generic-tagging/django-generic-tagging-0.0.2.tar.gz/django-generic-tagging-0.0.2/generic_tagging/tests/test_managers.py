from django.core.exceptions import PermissionDenied
from django.test.testcases import TestCase
from generic_tagging.models import Tag, TaggedItem
from generic_tagging.tests.factories import TagFactory, TaggedItemFactory, TagTestArticle0Factory, \
    TagTestArticle1Factory, UserFactory

from ..exceptions import CannotReorderException

from .compatibility import patch


class TagManagerTestCase(TestCase):
    def setUp(self):
        self.tag = TagFactory()
        self.other_tag = TagFactory()

    def test_get_for_object(self):
        article = TagTestArticle0Factory()
        other_article = TagTestArticle0Factory()

        TaggedItemFactory(tag=self.tag, content_object=article)
        TaggedItemFactory(tag=self.other_tag, content_object=article)
        TaggedItemFactory(tag=self.tag, content_object=other_article)
        TaggedItemFactory(tag=self.other_tag, content_object=other_article)

        tags0 = Tag.objects.get_for_object(article)
        self.assertEqual(tags0[0], self.tag)
        self.assertEqual(tags0[1], self.other_tag)

        tags1 = Tag.objects.get_for_object(other_article)
        self.assertEqual(tags1[0], self.tag)
        self.assertEqual(tags1[1], self.other_tag)

    def test_get_for_object_with_no_tag_article(self):
        article = TagTestArticle0Factory()
        tags = Tag.objects.get_for_object(article)
        self.assertEqual(len(tags), 0)


class TaggedItemManagerTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.article = TagTestArticle0Factory()
        self.other_article = TagTestArticle0Factory()

    def test_get_for_object(self):
        article = TagTestArticle0Factory()
        other_article = TagTestArticle0Factory()

        tagged_item0 = TaggedItemFactory(content_object=article)
        tagged_item1 = TaggedItemFactory(content_object=article)
        tagged_item2 = TaggedItemFactory(content_object=other_article)
        tagged_item3 = TaggedItemFactory(content_object=other_article)

        items0 = TaggedItem.objects.get_for_object(article)
        self.assertEqual(items0[0], tagged_item0)
        self.assertEqual(items0[1], tagged_item1)

        items1 = TaggedItem.objects.get_for_object(other_article)
        self.assertEqual(items1[0], tagged_item2)
        self.assertEqual(items1[1], tagged_item3)

    def test_add_with_not_permission(self):
        self.assertRaises(PermissionDenied, TaggedItem.objects.add, 'Tag name', self.article, self.user)

    def test_add_with_new_label(self):
        with patch.object(self.user, 'has_perm', return_value=True):
            before_tag_count = Tag.objects.count()
            tagged_item = TaggedItem.objects.add('Tag name', self.article, self.user)
            self.assertEqual(Tag.objects.count(), before_tag_count + 1)

            tags = Tag.objects.get_for_object(self.article)
            self.assertEqual(len(tags), 1)
            self.assertEqual(tags[0], Tag.objects.get(label='Tag name'))
            self.assertEqual(tagged_item.author, self.user)
            self.assertEqual(tagged_item.content_object, self.article)

    def test_add_with_exist_label(self):
        tag = TagFactory(label='Exist tag name')
        with patch.object(self.user, 'has_perm', return_value=True):
            before_tag_count = Tag.objects.count()
            tagged_item = TaggedItem.objects.add('Exist tag name', self.article, self.user)
            self.assertEqual(Tag.objects.count(), before_tag_count)

            tags = Tag.objects.get_for_object(self.article)
            self.assertEqual(len(tags), 1)
            self.assertEqual(tags[0], tag)
            self.assertEqual(tagged_item.author, self.user)
            self.assertEqual(tagged_item.content_object, self.article)

    def test_remove(self):
        item0 = TaggedItemFactory(tag__label='Unnecessary label', content_object=self.article)
        item1 = TaggedItemFactory(tag__label='Necessary label', content_object=self.article)
        TaggedItemFactory(tag__label='Unnecessary label', content_object=self.other_article)

        self.assertEqual(len(Tag.objects.get_for_object(self.article)), 2)
        self.assertEqual(len(Tag.objects.get_for_object(self.other_article)), 1)

        TaggedItem.objects.remove('Unnecessary label', self.article)
        self.assertEqual(len(Tag.objects.get_for_object(self.article)), 1)
        self.assertEqual(len(Tag.objects.get_for_object(self.other_article)), 1)
        self.assertNotIn(item0.tag, Tag.objects.get_for_object(self.article))
        self.assertIn(item1.tag, Tag.objects.get_for_object(self.article))

    def test_remove_with_not_attached_label(self):
        self.assertIsNone(TaggedItem.objects.remove('not exist tag', self.article))

    def test_clear(self):
        TaggedItemFactory(content_object=self.article)
        TaggedItemFactory(content_object=self.article)
        TaggedItemFactory(content_object=self.article)
        TaggedItemFactory(content_object=self.other_article)

        self.assertEqual(len(Tag.objects.get_for_object(self.article)), 3)
        self.assertEqual(len(Tag.objects.get_for_object(self.other_article)), 1)

        TaggedItem.objects.clear(self.article)

        self.assertEqual(len(Tag.objects.get_for_object(self.article)), 0)
        self.assertEqual(len(Tag.objects.get_for_object(self.other_article)), 1)

    def test_get_tag_count(self):
        TaggedItemFactory(content_object=self.article)
        TaggedItemFactory(content_object=self.article)
        TaggedItemFactory(content_object=self.article)
        TaggedItemFactory(content_object=self.other_article)

        self.assertEqual(TaggedItem.objects.get_tag_count(self.article), 3)
        self.assertEqual(TaggedItem.objects.get_tag_count(self.other_article), 1)

    def test_swap_tags(self):
        tagged_item0 = TaggedItemFactory(content_object=self.article, order=10)
        tagged_item1 = TaggedItemFactory(content_object=self.article, order=20)

        self.assertEqual(tagged_item0.order, 10)
        self.assertEqual(tagged_item1.order, 20)

        TaggedItem.objects.swap_order(tagged_item0, tagged_item1)
        self.assertEqual(tagged_item0.order, 20)
        self.assertEqual(tagged_item1.order, 10)

    def test_swap_tags_with_different_models(self):
        tagged_item0 = TaggedItemFactory(content_object=self.article, order=10)
        tagged_item1 = TaggedItemFactory(content_object=self.other_article, order=20)

        self.assertEqual(tagged_item0.order, 10)
        self.assertEqual(tagged_item1.order, 20)

        self.assertRaises(CannotReorderException, TaggedItem.objects.swap_order, tagged_item0, tagged_item1)

    def test_swap_tags_with_different_objects(self):
        other_model_article = TagTestArticle1Factory()
        tagged_item0 = TaggedItemFactory(content_object=self.article, order=10)
        tagged_item1 = TaggedItemFactory(content_object=other_model_article, order=20)

        self.assertEqual(tagged_item0.order, 10)
        self.assertEqual(tagged_item1.order, 20)

        self.assertRaises(CannotReorderException, TaggedItem.objects.swap_order, tagged_item0, tagged_item1)
