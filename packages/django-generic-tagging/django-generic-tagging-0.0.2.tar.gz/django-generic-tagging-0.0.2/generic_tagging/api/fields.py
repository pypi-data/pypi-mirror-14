from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from generic_tagging.models import Tag


class TagField(serializers.Field):
    def to_representation(self, obj):
        from generic_tagging.api.serializers import TagSerializer
        serializer = TagSerializer(obj)
        return serializer.data

    def to_internal_value(self, data):
        if isinstance(data, str):
            key = {'label': data}
        elif isinstance(data, dict):
            if 'label' in data:
                key = {'label': data['label']}
            else:
                raise ValidationError('tag parameter must contains label')
        (tag, created) = Tag.objects.get_or_create(**key)
        return tag
