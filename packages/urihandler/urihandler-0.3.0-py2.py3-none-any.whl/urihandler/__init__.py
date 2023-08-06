import logging
log = logging.getLogger(__name__)

from pyramid.config import Configurator

import os
import json
import yaml

from .handler import get_uri_handler, _build_uri_handler

def _parse_settings(settings):
    '''
    Parse the relevant settings for this application.

    :param dict settings:
    '''

    log.debug(settings)

    prefix='urihandler'

    defaults = {
        'config': os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'sample.yaml'))
    }

    urihand_settings = defaults.copy()

    for short_key_name in ('config', ):
        key_name = '%s.%s' % (prefix, short_key_name)
        if key_name in settings:
            urihand_settings[short_key_name] = \
                settings.get(key_name, defaults.get(short_key_name, None))

    for short_key in urihand_settings:
        long_key = '%s.%s' % (prefix, short_key)
        settings[long_key] = urihand_settings[short_key]

    return urihand_settings

def _load_configuration(path):
    '''
    Load the configuration for the UriHandler.

    :param str path: Path to the config file in YAML format.
    :returns: A :class:`dict` with the config options.
    '''
    log.debug('Loading uriregistry config from %s.' % path)
    f = open(path, 'r')
    content = yaml.load(f.read())
    log.debug(content)
    f.close()
    return content


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)

    urihand_settings = _parse_settings(config.registry.settings)
    handlerconfig = _load_configuration(urihand_settings['config'])

    _build_uri_handler(config.registry, handlerconfig)

    config.add_directive('get_uri_handler', get_uri_handler)
    config.add_request_method(get_uri_handler, 'uri_handler', reify=True)

    config.add_route('handle', '/handle')
    config.add_route('uris', '/uris')
    config.add_route('redirect', '/{uri:.*}')

    config.scan()
    return config.make_wsgi_app()
