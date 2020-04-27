"""
Models used for demographics collection.
"""

from django.contrib.auth import get_user_model
from django.db import models
from django_extensions.db.models import TimeStampedModel


User = get_user_model()


class DemographicsInfo(TimeStampedModel):
    """
    A django model used to track our learners demographic information.

    # TODO: Do I need to add the .pii declarations? I think I will, it would be silly that it is 
    # only for Will need to read OEP-30
    # See https://open-edx-proposals.readthedocs.io/en/latest/oep-0030-arch-pii-markup-and-auditing.html
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # TODO: localization/translation needed?
    GENDER_CHOICES = (
        ('f', 'Female'),
        ('m', 'Male'),
        ('nb', 'Non-binary/third gender'),
        ('pn', 'Prefer not to say'),
        # TODO: self-describe option?
    )
    gender = models.CharField(
        max_length=2,
        choices=GENDER_CHOICES,
        null=True,
    )
    
    TRANSGENDER_CHOICES = (
        ('y', 'Yes'),
        ('n', 'No'),
        ('pn', 'Prefer not to say'),
    )
    transgender = models.CharField(
        max_length=2,
        choices=TRANSGENDER_CHOICES,
        null=True,
    )
