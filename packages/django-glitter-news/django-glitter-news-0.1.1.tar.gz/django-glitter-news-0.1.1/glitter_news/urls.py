# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views, feeds


urlpatterns = [
    url(
        r'^$',
        views.PostListView.as_view(),
        name='list'
    ),
    url(
        r'^category/(?P<slug>[-\w]+)/$',
        views.PostListCategoryView.as_view(),
        name='post-list-category'
    ),
    url(
        r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        views.PostDetailView.as_view(),
        name='post-detail'
    ),
    url(
        r'^feed/$',
        feeds.NewsFeed(),
        name='feed'
    ),
    url(
        r'^feed/(?P<slug>[-\w]+)/$',
        feeds.NewsCategoryFeed(),
        name='category-feed'
    ),
]
