# -*- coding: utf-8 -*-

from django.utils import timezone
from haystack import indexes

from .models import Post


class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        return self.get_model().objects.published().select_related().filter(
            date__lte=timezone.now())
