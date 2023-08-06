from urllib.parse import quote
from django.test.testcases import TestCase
from django.core.urlresolvers import reverse
from generic_tagging.tests.factories import TagFactory


class TagListViewTestCase(TestCase):
    def test_list(self):
        tag0 = TagFactory()
        tag1 = TagFactory()

        url = reverse('generic_tagging_tag_list')
        self.assertEqual(url, '/')
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['object_list']), 2)
        self.assertEqual(r.context['object_list'][0], tag0)
        self.assertEqual(r.context['object_list'][1], tag1)


class TagDetailViewTestCase(TestCase):
    def test_detail(self):
        tag = TagFactory()

        url = reverse('generic_tagging_tag_detail', kwargs={'slug': tag.label})
        self.assertEqual(url, '/%s/' % quote(tag.label))
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context['object'], tag)
