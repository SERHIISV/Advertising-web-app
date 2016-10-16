from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from ads.views import AdsCityList, HomePage, Advert, Addition, AddCity

urlpatterns = [
    url(r'^$', HomePage.as_view(), name='home'),
    url(r'^city-ads/(?P<pk>\d+)/$', AdsCityList.as_view(), name='adverts'),
    url(r'^advert/(?P<pk>\d+)/$', Advert.as_view(), name='advert'),
    url(r'^addition/$', Addition.as_view(), name='addition'),
    url(r'^addcity/$', AddCity.as_view(), name='addcity'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
