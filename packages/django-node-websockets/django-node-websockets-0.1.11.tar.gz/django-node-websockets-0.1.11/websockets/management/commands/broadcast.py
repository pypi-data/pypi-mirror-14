import json
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from websockets.utils import get_emitter


class Command(BaseCommand):
    help = 'Emits a broadcast message to listening websockets'

    option_list = BaseCommand.option_list + (
        make_option(
            '--group',
            type="string",
            default=None,
            help='send only to this group',
        ),
    )
        # parser.add_argument('event', type=string)
        # parser.add_argument('content', type=string, default=None)
        # parser.add_argument('group', type=string, default=None)

    def handle(self, event, content="", *args, **options):
        io = get_emitter()
        if options['group']:
            io.To(options['group'])

        try:
            content = json.loads(content)
        except ValueError:
            content = content

        io.Emit(event, content)

        print("sent message", event, content)
