from __future__ import absolute_import

# django imports
from django.conf.urls import url, patterns

# authentication app imports
from disable_multidevice_login.apiviews import AppLoginAPIView
from disable_multidevice_login.apiviews import AppLogoutAPIView


urlpatterns = patterns(
    '',
    url(r'^(?P<version>(v1))/login/$',
        AppLoginAPIView.as_view(),
        name='app_login'),
    url(r'^(?P<version>(v1))/logout/$',
        AppLogoutAPIView.as_view(),
        name='app_logout'),
)
