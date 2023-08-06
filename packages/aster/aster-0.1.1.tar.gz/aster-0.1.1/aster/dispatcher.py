from aster.exceptions import *


def dispatch(method, api_name, request):
    # TODO: validate api_name

    try:
        api = __import__(api_name)
    except ImportError:
        raise APIEndpointNotFoundError()

    try:
        handler = getattr(api, method.lower())
    except AttributeError:
        raise NotImplementedHTTPMethodError()

    return handler(request)

