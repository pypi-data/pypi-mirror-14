from django.conf.urls import patterns, url, include
from generic_tagging.views import TagDetailView, TagListView


urlpatterns = patterns('',
                       url(r'^$',
                           TagListView.as_view(), name='generic_tagging_tag_list'),
                       url(r'^(?P<slug>[^/.+]+)/$',
                           TagDetailView.as_view(), name='generic_tagging_tag_detail'),
)
