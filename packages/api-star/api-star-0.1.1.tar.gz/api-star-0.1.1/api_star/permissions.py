from api_star.exceptions import Forbidden


def check_permissions(request, permissions):
    for permission in permissions:
        if not permission(request):
            raise Forbidden()


class IsAuthenticated(object):
    def __call__(self, request):
        return bool(request.auth)


class IsAuthenticatedOrReadOnly(object):
    def __call__(self, request):
        return bool(request.auth) or request.method in ('GET', 'HEAD', 'OPTIONS')
