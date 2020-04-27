"""
Demographics API v1 URLs.
"""

from django.conf.urls import include, url
from rest_framework import routers

from people.apps.demographics.rest_api.v1.views import DemographicsViewSet


router = routers.DefaultRouter()
router.register(r'demographics', DemographicsViewSet, basename='demographics')

urlpatterns = router.urls
