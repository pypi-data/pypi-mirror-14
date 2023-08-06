from pyramid.view import view_config

from pyramid.httpexceptions import (
    HTTPSeeOther,
    HTTPBadRequest,
    HTTPNotFound,
    HTTPNotModified
)

from urihandler.utils import create_version_hash


@view_config(route_name='redirect')
def redirect(request):
    uri = request.host_url + '/' + request.matchdict['uri']
    redirect = request.uri_handler.handle(uri, request)
    if not redirect:
        raise HTTPNotFound()
    return HTTPSeeOther(redirect)


@view_config(route_name='handle')
def handle(request):
    uri = request.params.get('uri', None)
    if not uri:
        raise HTTPBadRequest('Please include a URI parameter.')
    redirect = request.uri_handler.handle(uri, request)
    if not redirect:
        raise HTTPNotFound('Unknown URI.')
    return HTTPSeeOther(redirect)

@view_config(
    route_name='uris',
    renderer='json',
    accept='application/json',
    http_cache=(86400, {'public': True})
)
def uris(request):
    uri = request.params.get('uri', None)
    if not uri:
        raise HTTPBadRequest('Please include a URI parameter.')
    redirect = request.uri_handler.handle(uri, request)
    res = {
        'uri': uri,
        'success': redirect is not None,
        'location': redirect
    }
    etag = create_version_hash(res, request)
    request.response.headers['ETag'] = etag
    if 'If-None-Match' in request.headers:
        request.response.conditional_response = True
    return res
