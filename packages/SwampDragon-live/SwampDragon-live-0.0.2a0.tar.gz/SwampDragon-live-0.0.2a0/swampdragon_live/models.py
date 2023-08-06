# -*- coding: utf-8 -*-
from django.db.models.signals import post_save, pre_delete
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver

from .pushers import push_new_content_for_instance
from .pushers import push_new_content_for_queryset

@receiver(post_save)
def post_save_handler(sender, instance, **kwargs):
    if ContentType.objects.exists():
        instance_type = ContentType.objects.get_for_model(instance.__class__)

        push_new_content_for_queryset(queryset_type_pk=instance_type.pk,
                                      queryset_pk=instance.pk)

        push_new_content_for_instance(instance_type_pk=instance_type.pk,
                                      instance_pk=instance.pk)

@receiver(pre_delete)
def pre_delete_handler(sender, instance, **kwargs):
    if ContentType.objects.exists():
        instance_type = ContentType.objects.get_for_model(instance.__class__)

        push_new_content_for_queryset(queryset_type_pk=instance_type.pk,
                                      queryset_pk=instance.pk)
