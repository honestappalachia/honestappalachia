from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('wanted.views',
    url(r'^$', 'add_story', name="add_story"),
)
