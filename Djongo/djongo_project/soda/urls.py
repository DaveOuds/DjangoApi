from django.conf.urls import url
from soda import views

urlpatterns = [
    url(r'^sodas/$', views.soda_list),
    url(r'^soda/(?P<pk>[0-24]+)/$', views.soda_detail),
]