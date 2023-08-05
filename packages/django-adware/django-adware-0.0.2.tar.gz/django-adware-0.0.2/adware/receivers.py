from django.db import transaction
from django.db import IntegrityError

from . models import AdSense


def create_ad(sender, instance, created, *args, **kwargs):
    """
    Create an ad object upon user creation.
    """
    created = False
    try:
        obj = AdSense.objects.get(user=instance)
    except AdSense.DoesNotExist:
        try:
            with transaction.atomic():
                obj = AdSense.objects.create(user=instance)
                created = True
        except IntegrityError:
            obj = AdSense.objects.get(user=instance)
