import random

import gevent
from flask import Blueprint, render_template, Response

from ..ga.ga import GA

mod = Blueprint('gor0x', __name__,
                template_folder='templates',
                static_folder='static')


def compose_msg(**kwargs):
    prefix = "data: {\n"
    suffix =  'data: }\n\n'
    for k, v in kwargs.items():
        prefix += 'data: "{}": "{}", \n'.format(k, v)
    return prefix[:-3] + prefix[-2:] + suffix


def event_stream():
    while True:
        kwargs = {
            'id': random.randint(1, 100),
            'fitness': random.randint(1, 100)
        }
        gevent.sleep(2)
        yield compose_msg(**kwargs)


@mod.route('/event_source')
def sse_request():
    return Response(event_stream(), mimetype='text/event-stream')


@mod.route('/')
def index():
    return render_template('gor0x/index.html')