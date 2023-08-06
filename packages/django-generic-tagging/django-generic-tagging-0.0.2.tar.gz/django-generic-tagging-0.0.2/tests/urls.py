from django.conf.urls import patterns, url, include
from generic_tagging.api.routers import TaggingAPIRouter

router = TaggingAPIRouter(trailing_slash=True)

urlpatterns = patterns(r'',
    url(r'^api/', include(router.urls)),
    url(r'^', include('generic_tagging.urls'))
)
