from rest_framework import serializers

from .models import DemographicsInfo


class DemographicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemographicsInfo
        fields = (
            'id', 
            'user_id',
            'gender',
            'transgender',
        )
