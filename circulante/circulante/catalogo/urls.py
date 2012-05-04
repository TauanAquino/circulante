from django.conf.urls import patterns, include, url

from .views import search, catalog, edit

urlpatterns = patterns('',
    url(r'^search', search,name='search'),
    url(r'^catalog', catalog,name='catalog'),
    url(r'^edit/(\d+)', edit,name='edit'),
)
