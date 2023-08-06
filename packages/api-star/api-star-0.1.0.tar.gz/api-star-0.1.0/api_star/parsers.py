# coding: utf8
from __future__ import unicode_literals
from api_star.exceptions import BadRequest
from werkzeug.formparser import MultiPartParser as WerkzeugMultiPartParser
from werkzeug.formparser import default_stream_factory
from werkzeug.urls import url_decode_stream
import json


def _parse_params(content_type):
    """
    Parse the parameters out of a content-type header,
    returning them as a dictionary.
    """
    main_type, sep, param_string = content_type.partition(';')
    params = {}
    for token in param_string.strip().split(','):
        key, sep, value = token.partition('=')
        key = key.strip()
        value = value.strip()
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
        if key:
            params[key] = value
    return params


class JSONParser(object):
    media_type = 'application/json'

    def __call__(self, stream, **context):
        data = stream.read().decode('utf-8')
        try:
            return json.loads(data)
        except ValueError:
            msg = 'Malformed JSON'
            raise BadRequest(msg)


class MultiPartParser(object):
    media_type = 'multipart/form-data'

    def __call__(self, stream, **context):
        content_type = context['content_type']
        content_length = context['content_length']
        multipart_parser = WerkzeugMultiPartParser(default_stream_factory)

        params = _parse_params(content_type)
        boundary = params.get('boundary')
        if boundary is None:
            msg = 'Multipart message missing boundary in Content-Type header'
            raise BadRequest(msg)
        boundary = boundary.encode('ascii')

        try:
            data, files = multipart_parser.parse(stream, boundary, content_length)
        except ValueError:
            msg = 'Malformed multipart request'
            raise BadRequest(msg)

        data.update(files)
        return data


class URLEncodedParser(object):
    media_type = 'application/x-www-form-urlencoded'

    def __call__(self, stream, **context):
        return url_decode_stream(stream)
