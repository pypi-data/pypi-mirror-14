# -*- coding: utf-8 -*-

from .models import Post


class PostMixin(object):
    def get_queryset(self):
        return Post.objects.published()
