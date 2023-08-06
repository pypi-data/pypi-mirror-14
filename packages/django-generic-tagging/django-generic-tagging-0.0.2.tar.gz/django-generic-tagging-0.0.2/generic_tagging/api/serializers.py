from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from rest_framework import serializers

from generic_tagging.api.fields import TagField
from ..models import Tag, TaggedItem


class ContentObjectSerializer(serializers.Serializer):
    content_type = serializers.SerializerMethodField()
    object_id = serializers.SerializerMethodField(read_only=True)
    str = serializers.SerializerMethodField(read_only=True)
    url = serializers.SerializerMethodField(read_only=True)

    def get_content_type(self, obj):
        ct = ContentType.objects.get_for_model(obj)
        return ct.pk

    def get_object_id(self, obj):
        return obj.pk

    def get_url(self, obj):
        if not hasattr(obj, 'get_absolute_url'):
            return None
        return obj.get_absolute_url()

    def get_str(self, obj):
        return str(obj)


class TagSerializer(serializers.ModelSerializer):
    url = serializers.URLField(source='get_absolute_url', read_only=True)

    class Meta:
        model = Tag
        fields = ('id', 'label', 'url')
        extra_kwargs = {'id': {'read_only': True}}


class TaggedItemSerializer(serializers.ModelSerializer):
    content_type = serializers.PrimaryKeyRelatedField(queryset=ContentType.objects.all())
    created_at = serializers.DateTimeField(read_only=True)
    content_object = ContentObjectSerializer(read_only=True)
    detail_api_url = serializers.SerializerMethodField(read_only=True)
    lock_api_url = serializers.SerializerMethodField(read_only=True)
    unlock_api_url = serializers.SerializerMethodField(read_only=True)
    tag = TagField()

    def get_detail_api_url(self, obj):
        return reverse('taggeditem-detail', args=[obj.pk,])

    def get_lock_api_url(self, obj):
        return reverse('taggeditem-lock', args=[obj.pk,])

    def get_unlock_api_url(self, obj):
        return reverse('taggeditem-unlock', args=[obj.pk,])

    class Meta:
        model = TaggedItem
        fields = (
            'id', 'content_type', 'object_id', 'content_object',
            'author', 'locked', 'created_at',
            'tag', 'detail_api_url', 'lock_api_url', 'unlock_api_url'
        )
