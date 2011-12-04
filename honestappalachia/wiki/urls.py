from django.conf.urls.defaults import patterns, include, url

from templatetags.wiki import WIKI_WORD

urlpatterns = patterns('wiki.views',
    url(r'^$', 'index', name="index"),
    url(r'^(?P<name>%s)/$' % WIKI_WORD, 'view', name="view"),
    url(r'^(?P<name>%s)/edit/$' % WIKI_WORD, 'edit', name="edit"),
    url(r'^media/$', 'media_index', name="media_index"),
    url(r'^media/upload/$', 'media_upload', name="media_upload"),
)
