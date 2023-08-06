from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils.translation import ugettext_lazy as _
from rest_framework import viewsets
from rest_framework import status
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from rest_framework.renderers import JSONRenderer
from generic_tagging.api.serializers import TagSerializer, TaggedItemSerializer
from generic_tagging.models import Tag, TaggedItem


class TagViewSet(mixins.CreateModelMixin,
                 mixins.RetrieveModelMixin,
                 mixins.DestroyModelMixin,
                 mixins.ListModelMixin,
                 viewsets.GenericViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    renderer_classes = (JSONRenderer,)


class TaggedItemViewSet(mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    serializer_class = TaggedItemSerializer
    queryset = TaggedItem.objects.all()
    renderer_classes = (JSONRenderer,)

    def get_queryset(self):
        qs = super().get_queryset()
        object_id = self.request.query_params.get('object_id', None)
        content_type = self.request.query_params.get('content_type', None)
        if object_id and content_type:
            qs = qs.filter(object_id=object_id, content_type=content_type)
        return qs

    def list(self, request, *args, **kwargs):
        object_id = self.request.query_params.get('object_id', None)
        content_type = self.request.query_params.get('content_type', None)
        if not (content_type and object_id):
            return Response('Query parameters must contain content_type and object_id.',
                            status=status.HTTP_400_BAD_REQUEST)
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        object_id = self.request.data.get('object_id', None)
        content_type = self.request.data.get('content_type', None)
        label = self.request.data.get('tag', '')
        if label == '':
            return Response(_("Tag label is required."), status=status.HTTP_400_BAD_REQUEST)
        try:
            item = TaggedItem.objects.get(object_id=object_id, content_type=content_type, tag__label=label)
            return Response(_("'%s' is already added." % label), status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            pass
        return super().create(request, *args, **kwargs)

    def _get_extra_fields(self):
        extra_fields = {}
        if self.request.user.is_authenticated():
            extra_fields.update({'author': self.request.user})
        return extra_fields

    def perform_create(self, serializer):
        extras = self._get_extra_fields()
        serializer.save(**extras)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.locked:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return super().destroy(request, *args, **kwargs)

    @detail_route(methods=['patch'])
    def lock(self, request, pk):
        item = self.get_object()
        try:
            item.lock()
            serializer = TaggedItemSerializer(item)
            return Response(serializer.data)
        except ValidationError:
            return Response('the tag is already locked',
                            status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['patch'])
    def unlock(self, request, pk):
        item = self.get_object()
        try:
            item.unlock()
            serializer = TaggedItemSerializer(item)
            return Response(serializer.data)
        except ValidationError:
            return Response('the tag is already unlocked',
                            status=status.HTTP_400_BAD_REQUEST)
