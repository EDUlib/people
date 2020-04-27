"""
Demographics API URLs.
"""


from django.conf.urls import include, url


urlpatterns = [
    url(r'v1/', include(('people.apps.demographics.rest_api.v1.urls', 'v1'), namespace='v1')),
]
