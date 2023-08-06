# -*- coding: utf-8 -*-
from django.core.cache import InvalidCacheBackendError, caches
from django.contrib.contenttypes.models import ContentType
from django.template.loader import get_template
from django.template import Library
from django.db.models.query import QuerySet
from django.db.models import Model
import hashlib

from ..classes import ModelInstanceRef
from ..classes import ModelQuerySetRef
from ..classes import ContextRef

register = Library()

def getref_for_instance(instance):
    instance_type = ContentType.objects.get_for_model(instance.__class__)

    return ModelInstanceRef(instance_type.pk, instance.pk)

def getref_for_queryset(queryset):
    queryset_type = ContentType.objects.get_for_model(queryset.model)

    return ModelQuerySetRef(queryset_type.pk, queryset.query)

def listen_on_instance(channel_cache, tag_name, template_name, user, new_context, instance_ref):
    instance_type_pk = instance_ref.instance_type_pk
    instance_pk = instance_ref.instance_pk

    fragment_hash = hashlib.sha1('%s:%s' % (tag_name, template_name)).hexdigest()
    instance_hash = hashlib.sha1('%d:%d' % (instance_type_pk, instance_pk)).hexdigest()
    username_hash = hashlib.sha1('%d:%s' % (user.id, user.username)).hexdigest()
    user_cache_key = '%s-%s-%s' % (fragment_hash, instance_hash, username_hash)
    channel_cache.set(user_cache_key, (template_name, new_context))

    cache_key = 'swampdragon-live.type.%d.instance.%d' % (instance_type_pk, instance_pk)
    cache_keys = channel_cache.get(cache_key, set())
    cache_keys.add(user_cache_key)
    channel_cache.set(cache_key, set(cache_keys))

    return user_cache_key

def listen_on_queryset(channel_cache, tag_name, template_name, user, new_context, queryset_ref):
    queryset_type_pk = queryset_ref.queryset_type_pk
    queryset_dump = str(queryset_ref.query)

    fragment_hash = hashlib.sha1('%s:%s' % (tag_name, template_name)).hexdigest()
    queryset_hash = hashlib.sha1('%d:%s' % (queryset_type_pk, queryset_dump)).hexdigest()
    username_hash = hashlib.sha1('%d:%s' % (user.id, user.username)).hexdigest()
    user_cache_key = '%s-%s-%s' % (fragment_hash, queryset_hash, username_hash)
    data_cache_key = '%s-data' % user_cache_key
    channel_cache.set(data_cache_key, (template_name, new_context))
    channel_cache.set(user_cache_key, (queryset_ref, data_cache_key))

    cache_key = 'swampdragon-live.type.%d.queryset' % queryset_type_pk
    cache_keys = channel_cache.get(cache_key, set())
    cache_keys.add(user_cache_key)
    channel_cache.set(cache_key, set(cache_keys))

    return user_cache_key

@register.simple_tag(takes_context=True)
def include_live(context, tag_name, template_name, **kwargs):
    user = context['user']
    kwargs['user'] = user

    try:
        channel_cache = caches['swampdragon-live']
    except InvalidCacheBackendError:
        channel_cache = caches['default']

    new_context_data = {}
    for key, value in kwargs.items():
        if isinstance(value, Model):
            new_context_data[key] = getref_for_instance(instance=value)
        elif isinstance(value, QuerySet):
            new_context_data[key] = getref_for_queryset(queryset=value)
        else:
            new_context_data[key] = value

    new_context = ContextRef(new_context_data)

    user_cache_keys = []
    for value in new_context_data.values():
        if isinstance(value, ModelInstanceRef):
            user_cache_key = listen_on_instance(channel_cache, tag_name, template_name,
                                                user, new_context, instance_ref=value)
            user_cache_keys.append(user_cache_key)
        elif isinstance(value, ModelQuerySetRef):
            user_cache_key = listen_on_queryset(channel_cache, tag_name, template_name,
                                                user, new_context, queryset_ref=value)
            user_cache_keys.append(user_cache_key)

    channels = map(lambda c: 'swampdragon-live-%s' % c, user_cache_keys)
    classes = 'swampdragon-live %s' % ' '.join(channels)

    content = '<%s class="%s">' % (tag_name, classes)
    content += get_template(template_name).render(new_context)
    content += '</%s>' % tag_name
    return content
