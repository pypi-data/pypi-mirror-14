# -*- coding: utf-8 -*-
from swampdragon.pubsub_providers.data_publisher import publish_data
from django.core.cache import InvalidCacheBackendError, caches
from django.template.loader import get_template

try: # for Django 1.9+
    from django.db import transaction
    on_commit = transaction.on_commit
except: # for Django 1.6-1.8 with django-transaction-hooks
    from django.db import connection
    on_commit = connection.on_commit

def get_channel_cache():
    try:
        channel_cache = caches['swampdragon-live']
    except InvalidCacheBackendError:
        channel_cache = caches['default']
    return channel_cache

def push_new_content_for_instance(instance_type_pk, instance_pk):
    channel_cache = get_channel_cache()

    cache_key = 'swampdragon-live.type.%d.instance.%d' % (instance_type_pk, instance_pk)
    user_cache_keys = channel_cache.get(cache_key, [])

    for user_cache_key in user_cache_keys:
        channel = 'swampdragon-live-%s' % user_cache_key
        push_new_content(channel_cache, channel, user_cache_key)

def push_new_content_for_queryset(queryset_type_pk, queryset_pk):
    channel_cache = get_channel_cache()

    cache_key = 'swampdragon-live.type.%d.queryset' % (queryset_type_pk)
    user_cache_keys = channel_cache.get(cache_key, [])

    for user_cache_key in user_cache_keys:
        queryset_ref, data_cache_key = channel_cache.get(user_cache_key, (None, None))
        if queryset_ref and data_cache_key:
            if queryset_ref.resolve().filter(pk=queryset_pk).exists():
                channel = 'swampdragon-live-%s' % user_cache_key
                push_new_content(channel_cache, channel, data_cache_key)

def push_new_content(channel_cache, channel, cache_key):
    template_name, new_context = channel_cache.get(cache_key, (None, None))
    if template_name and new_context:
        def push():
            value = get_template(template_name).render(new_context)
            publish_data(channel=channel, data=value)
        on_commit(push)
