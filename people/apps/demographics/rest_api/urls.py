"""
Demographics API URLs.
"""


from django.conf.urls import include, url

app_name = "people.apps.demographics"

url_patterns = [
    url(r'^v1/', include('demographics.rest_api.v1.urls', namespace='v1')),
]
