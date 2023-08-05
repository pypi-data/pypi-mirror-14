from django.conf import settings
from django.conf.urls import *
from django.contrib import admin
from django.conf.urls.static import static

from .views import HomePage

admin.autodiscover()

STATIC_DOC_ROOT = settings.BASE_DIR + '/media'

urlpatterns = [
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/',     admin.site.urls),
    url(r'^$',          HomePage.as_view()),
    url(r'^',           include('relay.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
