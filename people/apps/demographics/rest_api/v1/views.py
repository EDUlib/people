""" 
API views 
"""

from edx_rest_framework_extensions.auth.jwt.authentication import (
    JwtAuthentication,
)
from rest_framework import generics, mixins, permissions, viewsets

from people.apps.demographics.models import DemographicsInfo
from people.apps.demographics.rest_api.serializers import DemographicsSerializer
from people.apps.demographics.rest_api.v1.permissions import (
    CanAccessDemographics,
)


# class DemographicsViewSet(mixins.CreateModelMixin,
#                           mixins.RetrieveModelMixin,
#                           mixins.UpdateModelMixin,
#                           mixins.DestroyModelMixin,
#                           viewsets.GenericViewSet):
# TODO: Remove ModelViewSet after testing initial POST/GET pieces, GET for a List needs to be disabled
class DemographicsViewSet(viewsets.ModelViewSet):
    """
    View for CRUD operations for data related to user-specific demographics data.

    List endpoints are restricted as the data is sensitive PII information.

    A user should only ever have access to updating and removing their own demographics 
    information. 
    """
    # authentication_classes = (JwtAuthentication, )
    permission_classes = (permissions.IsAuthenticated, CanAccessDemographics,)
    serializer_class = DemographicsSerializer
    queryset = DemographicsInfo.objects.all()
