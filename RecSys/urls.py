from django.conf.urls import patterns, include, url
from django.contrib import admin


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'principal.views.inicio', name='inicio'),
    url(r'^populate/', 'principal.views.populateDB'),
    url(r'^search/', 'principal.views.buscarPorUsuario'),
    url(r'^mejorpuntuados/', 'principal.views.mejorPuntuados'),
    url(r'^recomendados/', 'principal.views.'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
