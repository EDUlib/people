from rest_framework import serializers

from people.apps.demographics.models import DemographicsInfo

from django.contrib.auth.models import User


class DemographicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemographicsInfo
        fields = ('user', 'gender', 'transgender')
