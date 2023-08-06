from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied, ValidationError
from django.test.testcases import TestCase
from django.contrib.auth.models import User, Permission

from generic_tagging.exceptions import CannotDeleteLockedTagException
from generic_tagging.models import Tag, TaggedItem, TagManager, TaggedItemManager
from generic_tagging.tests.factories import TagFactory, TaggedItemFactory, \
    TagTestArticle0Factory, TagTestArticle1Factory

from .factories import UserFactory


class TagTestCase(TestCase):
    def test_manager(self):
        self.assertIsInstance(Tag.objects, TagManager)

    def test_str(self):
        tag = TagFactory(label='Test')
        self.assertEqual(str(tag), tag.label)

    def test_order(self):
        tag0 = TagFactory(label='banana')
        tag1 = TagFactory(label='apple')
        tag2 = TagFactory(label='cherry')
        tags = Tag.objects.all()
        self.assertEqual(tags[0], tag1)
        self.assertEqual(tags[1], tag0)
        self.assertEqual(tags[2], tag2)

    def test_get_absolute_url(self):
        tag = TagFactory()
        url = reverse('generic_tagging_tag_detail', kwargs={'slug': tag.label})
        self.assertEqual(tag.get_absolute_url(), url)

    def test_items(self):
        tag = TagFactory()
        item0 = TaggedItemFactory(content_object=TagTestArticle0Factory(), tag=tag)
        item1 = TaggedItemFactory(content_object=TagTestArticle1Factory(), tag=tag)
        self.assertEqual(tag.items.count(), 2)
        self.assertEqual(tag.items.all()[0], item0)
        self.assertEqual(tag.items.all()[1], item1)


class TaggedItemTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_manager(self):
        self.assertIsInstance(TaggedItem.objects, TaggedItemManager)

    def test_str(self):
        item = TaggedItemFactory(tag__label='Label')
        self.assertEqual(str(item), 'Label TagTestArticle0 object')

    def test_order(self):
        item0 = TaggedItemFactory(order=2)
        item1 = TaggedItemFactory(order=5)
        item2 = TaggedItemFactory(order=0)
        items = TaggedItem.objects.all()
        self.assertEqual(items[0], item2)
        self.assertEqual(items[1], item0)
        self.assertEqual(items[2], item1)

    def test_lock(self):
        item = TaggedItemFactory()
        self.assertFalse(item.locked)

        item.lock()
        self.assertTrue(item.locked)

    def test_lock_with_locked_item(self):
        item = TaggedItemFactory(locked=True)
        self.assertTrue(item.locked)

        self.assertRaises(ValidationError, item.lock)

    def test_unlock(self):
        item = TaggedItemFactory(locked=True)
        self.assertTrue(item.locked)

        item.unlock()
        self.assertFalse(item.locked)

    def test_unlock_with_not_locked_item(self):
        item = TaggedItemFactory()
        self.assertFalse(item.locked)

        self.assertRaises(ValidationError, item.unlock)

    def test_delete_for_unlocked_item(self):
        item = TaggedItemFactory()
        self.assertIn(item, TaggedItem.objects.all())

        item.delete()
        self.assertNotIn(item, TaggedItem.objects.all())

    def test_delete_for_locked_item(self):
        item = TaggedItemFactory(locked=True)
        self.assertIn(item, TaggedItem.objects.all())

        self.assertRaises(CannotDeleteLockedTagException, item.delete)
        self.assertIn(item, TaggedItem.objects.all())

    def test_related_name_for_tag(self):
        tag = TagFactory()
        item0 = TaggedItemFactory(tag=tag)
        item1 = TaggedItemFactory(tag=tag)
        TaggedItemFactory()
        self.assertEqual(tag.items.count(), 2)
        self.assertEqual(tag.items.all()[0], item0)
        self.assertEqual(tag.items.all()[1], item1)

    def test_related_name_for_author(self):
        item0 = TaggedItemFactory(author=self.user)
        item1 = TaggedItemFactory(author=self.user)
        TaggedItemFactory()

        self.assertEqual(self.user.items.count(), 2)
        self.assertEqual(self.user.items.all()[0], item0)
        self.assertEqual(self.user.items.all()[1], item1)
