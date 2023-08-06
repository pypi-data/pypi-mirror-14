# coding: utf8
from __future__ import unicode_literals
from api_star.compat import string_types, text_type
from api_star.utils import JSONEncoder
from coreapi.codecs import CoreJSONCodec
import jinja2
import json


def render(request, data):
    """
    Given the incoming request, and the outgoing data,
    determine the content type and content of the response.
    """
    renderer = request.renderer or request.renderers[0]

    if data is None:
        content = b''
    elif not isinstance(data, string_types):
        context = {'request': request}
        content = renderer(data, **context)
    else:
        content = data

    if isinstance(content, text_type) and renderer.charset:
        content = content.encode(renderer.charset)

    if renderer.media_type:
        content_type = '%s' % renderer.media_type
        if renderer.charset:
            content_type += '; charset=%s' % renderer.charset
    else:
        content_type = None

    return (content, content_type)


class JSONRenderer(object):
    media_type = 'application/json'
    charset = None
    format = 'json'

    def __call__(self, data, **context):
        return json.dumps(data, cls=JSONEncoder, ensure_ascii=False)


class CoreJSONRenderer(object):
    media_type = 'application/vnd.coreapi+json'
    charset = None
    format = 'coreapi'

    def __call__(self, data, **context):
        return CoreJSONCodec().dump(data)


class DocsRenderer(object):
    media_type = 'text/html'
    charset = 'utf-8'
    format = 'html'

    def __init__(self):
        loader = jinja2.PackageLoader('api_star', 'templates')
        env = jinja2.Environment(loader=loader)
        self.template = env.get_template('docs.html')

    def __call__(self, data, **context):
        return self.template.render(document=data)


class HTMLRenderer(object):
    media_type = 'text/html'
    format = 'html'

    def __call__(self, data, **context):
        return data
