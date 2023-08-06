from __future__ import print_function

import json
import urllib

import requests
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.core.cache import cache
from django.http.response import HttpResponse
from django.utils.decorators import method_decorator
from django.utils.functional import SimpleLazyObject
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from .utils import get_emitter


class WebsocketMixin(object):
    async_only = not settings.DEBUG

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):

        # not great security,
        # but should keep away most unwanted traffic
        if self.async_only and not request.META.get("HTTP_X_WEBSOCKET"):
            return HttpResponse(
                "Request not sent from async server",
                status=400
            )

        self.data = request.POST

        self.socket_id = self.data.get("socket")

        return super(WebsocketMixin, self).dispatch(request, *args, **kwargs)

    @classmethod
    def send_packet(cls, groups, event, data=None, request=None):

        io = get_emitter()
        if io:
            if groups:
                group_names = []
                for group in groups:
                    if isinstance(group, User):
                        group_names.append("users/{}".format(group.username))
                    elif hasattr(group, "session"):
                        if group.user.is_authenticated:
                            group_names.append(
                                "users/{}".format(group.user.username))
                        group_names.append(
                            "sessions/{}".format(group.session.session_key))
                    else:
                        group_names.append(group)
                print("sending to groups", group_names)
                io.To(group_names)
            print("sending", event)
            io.EmitSafe(event, data)
        else:
            print("no io!")

    def reply(self, event, data=None):
        """ send this event back to the caller's sockets """
        self.send_packet([self.request], event, data)

    def handle(self, data, *args, **kwargs):
        pass  # override me

    def post(self, request, *args, **kwargs):
        self.handle(self.data, *args, **kwargs)

        return HttpResponse("OK")

    # TODO: for debugging only
    get = post


class WebsocketView(WebsocketMixin, View):
    pass


class TaskWebsocketMixin(WebsocketMixin):
    task_name = "Task"
    task_event = "message"
    task_description = ""

    def get_task_description(self):
        return self.task_description

    def progress(self, percent, description=None, link=None):
        if percent < 1:
            percent *= 100
        self.send_packet(self.request.user, self.task_event, dict(
            status="progress",
            percent=percent,
            task=self.task_name,
            description=description or self.get_task_description(),
            link=link
        ))

    def finished(self, description=None, link=None, link_text=None):
        description = description or self.get_task_description()
        self.send_packet(self.request.user, self.task_event, dict(
            status="complete",
            percent=100,
            task=self.task_name,
            description=description or self.get_task_description(),
            link=link,
            link_text=link_text
        ))


class DefaultWebsocketView(WebsocketView):

    def post(self, request, event=None):
        join = []

        try:
            if event == "user":
                self.send_packet([request], "user", {"user": request.user.username})
            elif event == "disconnect":
                pass
            elif event == "echo":
                self.send_packet([request], "echo", self.data)

            if request.user.is_authenticated:
                join.append("users/{}".format(request.user.username))

            join.append("sessions/{}".format(request.session.session_key))
        except Exception as ex:
            print("exception", ex)

        return HttpResponse(json.dumps(dict(
            event="__cmd__",
            join=join
        )))
