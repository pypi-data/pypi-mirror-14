from rest_framework import routers
from generic_tagging.api.viewsets import TagViewSet, TaggedItemViewSet


class TaggingAPIRouter(routers.SimpleRouter):
    def __init__(self, trailing_slash=False):
        super().__init__(trailing_slash)
        self.register(r'tags', TagViewSet)
        self.register(r'tagged_items', TaggedItemViewSet)
