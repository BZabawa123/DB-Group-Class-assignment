# accounts/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import StudentsRSOs

@receiver(post_save, sender=StudentsRSOs)
def update_rso_status_after_insert(sender, instance, created, **kwargs):
    if created:
        instance.rso.update_status()

@receiver(post_delete, sender=StudentsRSOs)
def update_rso_status_after_delete(sender, instance, **kwargs):
    instance.rso.update_status()
