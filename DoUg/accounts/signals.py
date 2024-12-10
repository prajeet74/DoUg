from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group

# Signal to automatically assign new users to the "Student" group
@receiver(post_save, sender=User)
def add_to_customersr_group(sender, instance, created, **kwargs):
    if created:
        customers_group, _ = Group.objects.get_or_create(name='customers')
        instance.groups.add(customers_group)