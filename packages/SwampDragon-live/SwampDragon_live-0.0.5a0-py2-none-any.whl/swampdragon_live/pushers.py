# -*- coding: utf-8 -*-
from swampdragon.pubsub_providers.data_publisher import publish_data
from django.core.cache import InvalidCacheBackendError, caches
from django.template.loader import get_template
import hashlib

from .utils import get_channel_cache

def push_new_content_for_instance(instance_type_pk, instance_pk):
    channel_cache = get_channel_cache()

    instance_hash = hashlib.sha1('%d:%d' % (instance_type_pk, instance_pk)).hexdigest()

    cache_key_glob = 'sdl.user.%s-*' % instance_hash

    for user_cache_key in channel_cache.iter_keys(cache_key_glob):
        channel = user_cache_key.replace('sdl.user.', 'swampdragon-live-')
        yield lambda: push_new_content(channel_cache, channel, user_cache_key)

def push_new_content_for_queryset(queryset_type_pk, queryset_pk):
    channel_cache = get_channel_cache()

    queryset_hash = hashlib.sha1('%d:qs' % queryset_type_pk).hexdigest()

    cache_key_glob = 'sdl.user.%s-*' % queryset_hash

    for user_cache_key in channel_cache.iter_keys(cache_key_glob):
        queryset_ref, data_cache_key = channel_cache.get(user_cache_key, (None, None))
        if queryset_ref and data_cache_key:
            if queryset_ref.resolve().filter(pk=queryset_pk).exists():
                channel = user_cache_key.replace('sdl.user.', 'swampdragon-live-')
                yield lambda: push_new_content(channel_cache, channel, data_cache_key)

def push_new_content(channel_cache, channel, cache_key):
    template_name, new_context = channel_cache.get(cache_key, (None, None))
    if template_name and new_context:
        value = get_template(template_name).render(new_context)
        publish_data(channel=channel, data=value)
