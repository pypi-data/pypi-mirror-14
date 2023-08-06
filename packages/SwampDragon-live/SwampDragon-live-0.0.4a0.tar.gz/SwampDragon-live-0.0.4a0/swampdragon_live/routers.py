# -*- coding: utf-8 -*-
from swampdragon import route_handler
from swampdragon.route_handler import BaseRouter
import hashlib

class LiveTemplateRouter(BaseRouter):
    route_name = 'swampdragon-live'
    valid_verbs = ['subscribe', 'unsubscribe']

    def get_subscription_channels(self, key, **kwargs):
        if key.startswith('swampdragon-live-'):
            user = self.connection.get_user()
            if user:
                username_hash = hashlib.sha1('%d:%s' % (user.id, user.username)).hexdigest()
                if username_hash:
                    if key.split('-')[-1] == username_hash:
                        return [key]
        return []

route_handler.register(LiveTemplateRouter)
