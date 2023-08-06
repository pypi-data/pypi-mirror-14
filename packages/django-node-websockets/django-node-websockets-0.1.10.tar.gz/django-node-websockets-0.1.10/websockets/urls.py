from django.conf.urls import patterns, url
from .views import DefaultWebsocketView


urlpatterns = patterns('',
    url(r'(?P<event>[\w\-_]+)', DefaultWebsocketView.as_view())
)
