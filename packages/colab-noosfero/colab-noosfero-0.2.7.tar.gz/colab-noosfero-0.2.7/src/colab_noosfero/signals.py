from django.db.models.signals import pre_save
from django.dispatch import receiver
from colab_noosfero.models import NoosferoSoftwareCommunity
from django.core.exceptions import ObjectDoesNotExist
from colab.signals.signals import send


@receiver(pre_save, sender=NoosferoSoftwareCommunity)
def verify_community_creation(sender, **kwargs):
    software_community = kwargs.get('instance')
    try:
        NoosferoSoftwareCommunity.objects.get(pk=software_community.id)
    except ObjectDoesNotExist:
        send('community_creation', 'noosfero',
             community=software_community.community)
    else:
        send('community_updated', 'noosfero',
             community=software_community.community)
