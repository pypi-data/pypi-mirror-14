from django.test.testcases import TestCase
from django.contrib.contenttypes.models import ContentType

from generic_tagging.models import TaggedItem, Tag
from generic_tagging.api.serializers import TagSerializer, TaggedItemSerializer, ContentObjectSerializer
from generic_tagging.tests.factories import TaggedItemFactory, UserFactory, TagTestArticle0Factory, TagFactory
from generic_tagging.tests.compatibility import patch


class ContentObjectSerializerTestCase(TestCase):
    def test_read(self):
        article = TagTestArticle0Factory()
        ct = ContentType.objects.get_for_model(article)
        with patch.object(article, 'get_absolute_url', create=True, return_value='absolute_url'):
            serializer = ContentObjectSerializer(article)
            data = serializer.data
            self.assertEqual(data, {
                'content_type': ct.pk,
                'object_id': article.pk,
                'url': 'absolute_url',
                'str': str(article)
            })


class TagSerializerTestCase(TestCase):
    def test_write(self):
        serializer = TagSerializer(data={'label': 'new label'})
        self.assertTrue(serializer.is_valid())
        serializer.save()


class TaggedItemSerializerTestCase(TestCase):
    def test_read(self):
        tagged_item = TaggedItemFactory()
        serializer = TaggedItemSerializer(tagged_item)
        data = serializer.data
        self.assertEqual(data['author'], tagged_item.author.pk)
        self.assertIsNotNone(data['created_at'])
        self.assertEqual(data['object_id'], tagged_item.object_id)
        self.assertEqual(data['content_type'], tagged_item.content_type.pk)
        self.assertFalse(data['locked'])
        self.assertEqual(data['tag']['id'], tagged_item.tag.pk)
        self.assertEqual(data['tag']['label'], tagged_item.tag.label)
        self.assertEqual(data['detail_api_url'], '/api/tagged_items/%d/' % tagged_item.pk)
        self.assertEqual(data['lock_api_url'], '/api/tagged_items/%d/lock/' % tagged_item.pk)
        self.assertEqual(data['unlock_api_url'], '/api/tagged_items/%d/unlock/' % tagged_item.pk)

    def test_write_with_new_tag(self):
        user = UserFactory()
        article = TagTestArticle0Factory()
        ct = ContentType.objects.get_for_model(article)

        tagged_item_count = TaggedItem.objects.count()
        tag_count = Tag.objects.count()
        serializer = TaggedItemSerializer(data={'author': user.pk, 'object_id': article.pk, 'content_type': ct.pk, 'tag': {'label': 'hoge'}})
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.errors, {})

        tagged_item = serializer.save()
        self.assertIsNotNone(tagged_item)
        self.assertEqual(TaggedItem.objects.count(), tagged_item_count + 1)
        self.assertEqual(Tag.objects.count(), tag_count + 1)

    def test_write_with_exist_tag(self):
        user = UserFactory()
        article = TagTestArticle0Factory()
        ct = ContentType.objects.get_for_model(article)
        tag = TagFactory()

        tagged_item_count = TaggedItem.objects.count()
        tag_count = Tag.objects.count()
        serializer = TaggedItemSerializer(data={'author': user.pk, 'object_id': article.pk, 'content_type': ct.pk, 'tag': {'label': tag.label}})
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.errors, {})

        tagged_item = serializer.save()
        self.assertIsNotNone(tagged_item)
        self.assertEqual(TaggedItem.objects.count(), tagged_item_count + 1)
        self.assertEqual(Tag.objects.count(), tag_count)
