from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from generic_tagging.models import Tag, TaggedItem


class TagDetailView(DetailView):
    model = Tag
    slug_field = 'label'


class TagListView(ListView):
    model = Tag
