from django.test import TestCase
from django.template import Template, Context
from django.contrib.contenttypes.models import ContentType
from django.template.loader import render_to_string
from .factories import TaggedItemFactory, TagTestArticle0Factory


class TaggingTemplateTagTestCase(TestCase):
    def test_get_tagged_items_for(self):
        article = TagTestArticle0Factory()
        item0 = TaggedItemFactory(content_object=article)
        item1 = TaggedItemFactory(content_object=article)

        t = Template(
            "{% load tagging %}"
            "{% get_tagged_items_for article as items %}"
        )
        context = Context({'article': article})
        r = t.render(context)
        self.assertEqual(r.strip(), '')
        self.assertEqual(len(context['items']), 2)
        self.assertEqual(context['items'][0], item0)
        self.assertEqual(context['items'][1], item1)

    def test_get_tags_for(self):
        article = TagTestArticle0Factory()
        item0 = TaggedItemFactory(content_object=article, tag__label='aaa')
        item1 = TaggedItemFactory(content_object=article, tag__label='bbb')

        t = Template(
            "{% load tagging %}"
            "{% get_tags_for article as tags %}"
        )
        context = Context({'article': article})
        r = t.render(context)
        self.assertEqual(r.strip(), '')
        self.assertEqual(len(context['tags']), 2)
        self.assertEqual(context['tags'][0], item0.tag)
        self.assertEqual(context['tags'][1], item1.tag)

    def test_get_content_type_for(self):
        article = TagTestArticle0Factory()

        t = Template(
            "{% load tagging %}"
            "{% get_content_type_for article as ct %}"
        )
        context = Context({'article': article})
        r = t.render(context)
        self.assertEqual(r.strip(), '')
        self.assertEqual(context['ct'], ContentType.objects.get_for_model(article))

    def test_render_generic_tagging_head_tag(self):
        t = Template(
            "{% load tagging %}"
            "{% render_generic_tagging_head_tag %}"
        )
        context = Context()
        r = t.render(context)
        self.assertEqual(r, render_to_string('generic_tagging/head.html'))

    def test_render_generic_tagging_component_tag_for(self):
        article = TagTestArticle0Factory()
        t = Template(
            "{% load tagging %}"
            "{% render_generic_tagging_component_tag_for article %}"
        )
        context = Context({'article': article})
        r = t.render(context)
        self.assertEqual(r, render_to_string('generic_tagging/component.html', {'object': article}))
