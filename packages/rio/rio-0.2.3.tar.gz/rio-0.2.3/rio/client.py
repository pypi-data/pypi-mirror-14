# -*- coding: utf-8 -*-

import logging

from requests import ConnectionError

from urlparse import urlparse
from rio.utils.http import urlopen

logger = logging.getLogger('rio.client')

def parse_netloc(netloc):
    auth, _netloc = netloc.split('@')
    sender, token = auth.split(':')
    domain, port = _netloc.split(':')
    port = int(port or 80)
    return dict(sender=sender, token=token, domain=domain, port=port)

def parse_path(path):
    version, project = path[1:].split('/')
    return dict(version=int(version), project=project)

def parse_dsn(dsn):
    parsed_dsn = urlparse(dsn)
    parsed_netloc = parse_netloc(parsed_dsn.netloc)
    parsed_path = parse_path(parsed_dsn.path)
    return {
        'scheme': parsed_dsn.scheme,
        'sender': parsed_netloc.get('sender'),
        'token': parsed_netloc.get('token'),
        'netloc': parsed_netloc.get('netloc'),
        'version': parsed_path.get('version'),
        'project': parsed_path.get('project'),
    }

class Client(object):

    def __init__(self, dsn):
        self.dsn = dsn
        self.context = parse_dsn(dsn)

    def emit(self, slug, payload):
        url = '%(scheme)s://%(domain)s:%(port)d/event/%(project)/emit/' % self.context
        url += slug
        return urlopen(url, 'POST', data=payload, timeout=3)
