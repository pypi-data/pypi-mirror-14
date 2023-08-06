# -*- coding: utf-8 -*-

import logging
log = logging.getLogger(__name__)

import re
import copy

from zope.interface import Interface


class IUriHandler(Interface):
    pass


class UriHandler:
    '''
    Central handler that deals with redirecting uri's.
    '''

    def __init__(self, uris=[]):
        self.uris = uris

    def handle(self, uri, request):
        uris = copy.deepcopy(self.uris)
        for u in uris:
            if 'mount' not in u or u['mount']:
                if u['match'].startswith('^'):
                    u['match'] = u['match'].replace('^', '^' + request.host_url)
                else:
                    u['match'] = request.host_url + '/.*' + u['match']
            log.debug('Matching {0} to {1}.'.format(uri, u['match']))
            m = re.match(u['match'], uri)
            if m:
                redirect = u['redirect'].format(**m.groupdict())
                log.debug('Match found. Redirecting to {0}.'.format(redirect,))
                return redirect
        return None


def _build_uri_handler(registry, handlerconfig):
    '''
    :param pyramid.registry.Registry registry: Pyramid registry
    :param dict handlerconfig: UriHandler config in dict form.
    :rtype: :class:`uriregistry.registry.UriHandler`
    '''
    uri_handler = registry.queryUtility(IUriHandler)
    if uri_handler is not None:
        return uri_handler

    uri_handler = UriHandler(
        handlerconfig['uris'],
    )

    registry.registerUtility(uri_handler, IUriHandler)
    return registry.queryUtility(IUriHandler)


def get_uri_handler(registry):
    '''
    Get the :class:`urihandler.handler.UriHandler` attached to this pyramid
    application.

    :rtype: :class:`urihandler.handler.UriHandler`
    '''
    # Argument might be a config or request
    regis = getattr(registry, 'registry', None)
    if regis is None:
        regis = registry
    return regis.queryUtility(IUriHandler)
