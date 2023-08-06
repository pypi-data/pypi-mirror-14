from django import template
from django.contrib.contenttypes.models import ContentType
from django.template.loader import render_to_string
from ..models import TaggedItem, Tag

register = template.Library()


@register.assignment_tag
def get_tagged_items_for(object):
    '''retrieve tagged items which relative with the specific object.
    :syntax: {% get_tagged_items_for <object> as <variable> %}
    '''
    return TaggedItem.objects.get_for_object(object)


@register.assignment_tag
def get_tags_for(object):
    '''retrieve tags which relative with the specific object.
    :syntax: {% get_tags_for <object> as <variable> %}
    '''
    return Tag.objects.get_for_object(object)


@register.assignment_tag
def get_content_type_for(object):
    '''retrieve content type object for the specific object.
    :syntax: {% get_content_type_for <object> as <variable> %}
    '''
    return ContentType.objects.get_for_model(object)


@register.simple_tag
def render_generic_tagging_head_tag():
    return render_to_string('generic_tagging/head.html')


@register.simple_tag
def render_generic_tagging_component_tag_for(object):
    return render_to_string('generic_tagging/component.html', {'object': object})
