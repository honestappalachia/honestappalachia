from django.conf.urls.defaults import patterns, include, url

from templatetags.wiki import WIKI_WORD

urlpatterns = patterns('wiki.views',
    url(r'^$', 'main_page', name="main_page"),
    url(r'^index/$', 'index', name="index"),
    url(r'^(?P<name>%s)/$' % WIKI_WORD, 'view', name="view"),
    url(r'^(?P<name>%s)/edit/$' % WIKI_WORD, 'edit', name="edit"),
    url(r'^(?P<name>%s)/delete/$' % WIKI_WORD, 'delete', name="delete"),
    url(r'^media/$', 'media_index', name="media_index"),
    url(r'^media/upload/$', 'media_upload', name="media_upload"),
)
