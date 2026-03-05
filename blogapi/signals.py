from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Post
from django.core.cache import cache

@receiver([post_save, post_delete], sender=Post)
def invalide_cache(sender, instance, **kwargs):
    print("Cache invalidated for post list")
    cache.delete_pattern("*post_list*")
