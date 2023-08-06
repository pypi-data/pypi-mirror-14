from api_star.exceptions import Unauthorized
import base64


class BasicAuthentication(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __call__(self, request):
        auth = request.headers.get('authorization', '').split()

        if not auth or auth[0].lower() != b'basic':
            return None

        if len(auth) == 1:
            msg = 'Invalid value in Authorization header. No credentials provided.'
            raise Unauthorized(msg)
        elif len(auth) > 2:
            msg = 'Invalid value in Authorization header. Credentials string should not contain spaces.'
            raise Unauthorized(msg)

        try:
            decoded = base64.b64decode(auth[1]).decode('iso-8859-1')
        except (TypeError, UnicodeDecodeError):
            msg = 'Invalid value in Authorization header. Credentials not correctly base64 encoded.'
            raise Unauthorized(msg)

        username, _, password = decoded.partition(':')
        return self.authenticate_credentials(username, password)

    def authenticate_credentials(self, username, password):
        if username != self.username or password != self.password:
            msg = 'Incorrect username or password.'
            raise Unauthorized(msg)

        return username


class TokenAuthentication(object):
    def __init__(self, username, token):
        self.username = username
        self.token = token

    def __call__(self, request):
        auth = request.headers.get('authorization', '').split()

        if not auth or auth[0].lower() != b'token':
            return None

        if len(auth) == 1:
            msg = 'Invalid token in Authorization header. No credentials provided.'
            raise Unauthorized(msg)
        elif len(auth) > 2:
            msg = 'Invalid token in Authorization header. Credentials string should not contain spaces.'
            raise Unauthorized(msg)

        try:
            token = auth[1].decode('iso-8859-1')
        except UnicodeDecodeError:
            msg = 'Invalid token in Authorization header. HTTP request headers must be ISO-8859-1 encoded.'
            raise Unauthorized(msg)

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, token):
        if token != self.token:
            msg = 'Incorrect token.'
            raise Unauthorized(msg)

        return self.username
