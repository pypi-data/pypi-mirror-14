# -*- coding: utf-8 -*-

from glitter.mixins import GlitterDetailMixin

from django.views.generic import ArchiveIndexView, DateDetailView
from django.shortcuts import get_object_or_404
from django.conf import settings

from .models import Category, Post
from .mixins import PostMixin


class PostListView(PostMixin, ArchiveIndexView):
    allow_empty = True
    date_field = 'date'
    paginate_by = getattr(settings, 'NEWS_PER_PAGE', 10)
    template_name_suffix = '_list'
    context_object_name = 'object_list'

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['news_categories'] = True
        return context


class PostListCategoryView(PostListView):
    template_name_suffix = '_category_list'

    def get_queryset(self):
        qs = super(PostListCategoryView, self).get_queryset()
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return qs.filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super(PostListCategoryView, self).get_context_data(**kwargs)
        context['current_category'] = self.category
        return context


class PostDetailView(GlitterDetailMixin, DateDetailView):
    queryset = Post.objects.select_related().filter(published=True)
    month_format = '%m'
    date_field = 'date_url'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()

        # Add this to display 'All news' on categories list.
        context['news_categories'] = True
        context['current_category'] = self.object.category
        return context

