# -*- coding: utf-8 -*-
from django.core.cache import InvalidCacheBackendError, caches
from django.contrib.contenttypes.models import ContentType
from django.template.loader import get_template
from django.template import Library
from django.db.models.query import QuerySet
from django.db.models import Model
import hashlib

from ..utils import get_channel_cache
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

    instance_hash = hashlib.sha1('%d:%d' % (instance_type_pk, instance_pk)).hexdigest()
    fragment_hash = hashlib.sha1('%s:%s' % (tag_name, template_name)).hexdigest()
    username_hash = hashlib.sha1('%d:%s' % (user.id, user.username)).hexdigest()
    cache_key = '%s-%s-%s' % (instance_hash, fragment_hash, username_hash)
    user_cache_key = 'sdl.user.%s' % cache_key
    refc_cache_key = 'sdl.refc.%s' % cache_key
    channel_cache.set(user_cache_key, (template_name, new_context))
    channel_cache.add(refc_cache_key, 0)

    return user_cache_key

def listen_on_queryset(channel_cache, tag_name, template_name, user, new_context, queryset_ref):
    queryset_type_pk = queryset_ref.queryset_type_pk
    queryset_dump = hashlib.sha1(str(queryset_ref.query)).hexdigest()

    queryset_hash = hashlib.sha1('%d:qs' % queryset_type_pk).hexdigest()
    fragment_hash = hashlib.sha1('%s:%s' % (tag_name, template_name)).hexdigest()
    username_hash = hashlib.sha1('%d:%s' % (user.id, user.username)).hexdigest()
    cache_key = '%s-%s-%s-%s' % (queryset_hash, queryset_dump, fragment_hash, username_hash)
    user_cache_key = 'sdl.user.%s' % cache_key
    data_cache_key = 'sdl.data.%s' % cache_key
    refc_cache_key = 'sdl.refc.%s' % cache_key
    channel_cache.set(data_cache_key, (template_name, new_context))
    channel_cache.set(user_cache_key, (queryset_ref, data_cache_key))
    channel_cache.add(refc_cache_key, 0)

    return user_cache_key

@register.simple_tag(takes_context=True)
def include_live(context, tag_name, template_name, **kwargs):
    user = context['user']
    kwargs['user'] = user

    channel_cache = get_channel_cache()

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

    make_channel = lambda c: c.replace('sdl.user.', 'swampdragon-live-')
    channels = map(make_channel, user_cache_keys)
    classes = 'swampdragon-live %s' % ' '.join(channels)

    content = '<%s class="%s">' % (tag_name, classes)
    content += get_template(template_name).render(new_context)
    content += '</%s>' % tag_name
    return content
