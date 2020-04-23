""" 
API views 
"""


import logging

from rest_framework import generics

from people.apps.demographics.models import DemographicsInfo
from people.apps.demographics.rest_api.serializers import DemographicsSerializer

log = logging.getLogger(__name__)


class DemographicsList(generics.ListCreateAPIView):
    serializer_class = DemographicsSerializer
    queryset = Demographics.objects.all()


class DemographicsDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DemographicsSerializer
    queryset = DemographicsInfo.objects.all()
