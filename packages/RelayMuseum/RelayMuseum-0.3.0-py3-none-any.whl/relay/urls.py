from django.conf.urls import *

from relay.models import *
from relay import views

urlpatterns = [
    url(r'^language/(?P<slug>[-a-z0-9._]+)/$', views.language_detail),
    url(r'^language/$', views.language_list),
    url(r'^relay/(?P<relay>[-a-z0-9._]+)/(?P<ring>[-a-z0-9._]+)/(?P<pk>[0-9]+)/$',
        views.torch_detail),
    url(r'^relay/(?P<relay>[-a-z0-9._]+)/(?P<ring>[-a-z0-9._]+)/([?](?P<action>smooth))?$',
        views.show_ring),
    url(r'^relay/(?P<slug>[-a-z0-9._]+)/$', views.relay_detail),
    url(r'^relay/$', views.relay_list),
    url(r'^participant/(?P<slug>[-a-z0-9._]+)/$', views.participant_detail),
    url(r'^participant/$', views.participant_list),
    url(r'^statistics/$', views.show_statistics),
]

