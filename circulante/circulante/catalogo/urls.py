from django.conf.urls import patterns, include, url

from .views import search, catalog

urlpatterns = patterns('',
    url(r'^search', search,name='search'),
    url(r'^catalog', catalog,name='catalog'),
)
