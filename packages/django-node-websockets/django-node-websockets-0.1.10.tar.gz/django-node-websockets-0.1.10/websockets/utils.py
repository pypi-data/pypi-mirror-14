import datetime
from urlparse import urlparse

from django.conf import settings

from emitter import Emitter


class SafeEmitter(Emitter):

    def make_safe(self, data):
        for key, value in data.items():
            if isinstance(value, dict):
                self.make_safe(value)
            if isinstance(value, datetime.datetime):
                data[key] = value.isoformat()
        return data

    def EmitSafe(self, event, data, **kwargs):
        return self.Emit(event, self.make_safe(data), **kwargs)


def get_emitter():
    if hasattr(settings, "SOCKETIO_REDIS"):
        if settings.SOCKETIO_REDIS:
            return SafeEmitter(settings.SOCKETIO_REDIS)
        return None
    else:
        location = urlparse(settings.CACHES['default']['LOCATION'])
        return SafeEmitter({"host": location.hostname, "port": location.port})
