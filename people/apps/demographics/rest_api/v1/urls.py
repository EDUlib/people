"""
Demographics API v1 URLs.
"""

from django.conf import settings
from django.conf.urls import include, url

from people.apps.demographics.rest_api.v1.views import DemographicsList, DemographicsDetailView

app_name = "people.apps.demographics"

urlpatterns = [
    url(
        r'^demographics/$',
        DemographicsList.as_view(),
        name='demographics'
    ),
    url(
        r'demographics/{user_id}/$'.format(user_id=settings.USER_ID_PATTERN),
        DemographicsDetailView.as_view(),
        name='demographics'
    )
]
