from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template, redirect_to
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'wikisite.views.home', name='home'),
    # url(r'^wikisite/', include('wikisite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    url(r'^$', direct_to_template, { 'template': 'home.html' }, name='home'),
    url(r'^about-us/$', direct_to_template, { 'template': 'about-us.html' },
        name="about-us"),
    url(r'^upload/$', 'honestappalachia.views.upload', name="upload"),
    url(r'^contact/$', direct_to_template, { 'template': 'contact.html' }, name="contact"),
    url(r'^donate/$', direct_to_template, { 'template': 'donate.html' }, name="donate"),

    #url(r'^wiki/', include('wiki.urls')),
)

# django.contrib.auth
urlpatterns += patterns('',
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name="login"),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', name="logout"),
    url(r'^accounts/profile/$', 'wiki.views.user_profile', name="profile"),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            { 'document_root': settings.MEDIA_ROOT }),
    )
