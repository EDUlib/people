"""
Models used for demographics collection.
"""


from django.db import models
from django_extensions.db.models import TimeStampedModel


class DemographicsInfo(TimeStampedModel):
    """
    A django model used to track our learners demographic information.

    # TODO: Do I need to add the .pii declarations? I think I will, it would be silly that it is 
    # only for Will need to read OEP-30
    # See https://open-edx-proposals.readthedocs.io/en/latest/oep-0030-arch-pii-markup-and-auditing.html
    """
    id = UnsignedBigIntAutoField(primary_key=true)
    user_id = models.IntegerField(blank=False) # TODO: db_index = True?

    GENDER_CHOICES = (
        ('f', _('Female')),
        ('m', _('Male')),
        ('nb', _('Non-binary/third gender')),
        ('pn', _('Prefer not to say')),
        # todo: self-describe option?
    )
    gender = models.CharField(
        max_length=2,
        choices=GENDER_CHOICES,
        null=True,
    )
    
    TRANSGENDER_CHOICES = (
        ('y', _('Yes')),
        ('n', _('No')),
        ('pn', _('Prefer not to say')),
    )
    transgender = models.CharField(
        max_length=2,
        choices=TRANSGENDER_CHOICES,
        null=True,
    )
