'''Sloth CI validator for `GitHub <https://github.com/>`_ push events.

Installation
------------

.. code-block:: bash

    $ pip install sloth-ci.validators.github


Usage
-----

.. code-block:: yaml

    provider:
        github:
            # Repository owner. Mandatory parameter.
            owner: moigagoo

            # Repository title as it appears in the URL, i.e. slug.
            # Mandatory parameter.
            repo: sloth-ci

            # Only pushes to these branches will initiate a build.
            # Skip this parameter to allow all branches to fire builds.
            branches:
                - master
                - staging
'''


__title__ = 'sloth-ci.validators.github'
__description__ = 'GitHub validator for Sloth CI'
__version__ = '1.1.1'
__author__ = 'Konstantin Molchanov'
__author_email__ = 'moigagoo@live.com'
__license__ = 'MIT'


def validate(request, validation_data):
    '''Check payload from GitHub: the origin IP must be genuine; the repo owner and title must be valid.

    :param request: `CherryPy request <http://docs.cherrypy.org/en/latest/pkg/cherrypy.html#cherrypy._cprequest.Request>`_ instance representing incoming request
    :param validation_data: dict with the keys ``owner``, ``repo``, and ``branches``, parsed from the config

    :returns: namedtuple(status, message, list of extracted params as dicts), e.g. ``Response(status=200, message='Payload validated. Branches: default', [{'branch': 'default'}])``
    '''

    from collections import namedtuple

    from ipaddress import ip_address, ip_network

    response = namedtuple('Response', ('status', 'message', 'param_dicts'))

    if request.method != 'POST':
        return response(
            405,
            'Payload validation failed: Wrong method, POST expected, got %s.' %
            request.method,
            [])

    trusted_ips = ip_network('192.30.252.0/22')

    remote_ip = ip_address(request.remote.ip)

    if remote_ip not in trusted_ips:
        return response(
            403,
            'Payload validation failed: Unverified remote IP: %s.' %
            remote_ip,
            [])

    try:
        payload = request.json

        is_ping = 'zen' in payload

        if is_ping:
            owner = payload['repository']['owner']['login']
        else:
            owner = payload['repository']['owner']['name']

        if owner != validation_data['owner']:
            return response(
                403, 'Payload validation failed: wrong owner: %s' % owner, [])

        repo = payload['repository']['name']

        if repo != validation_data['repo']:
            return response(
                403, 'Payload validation failed: wrong repository: %s' %
                repo, [])

        if is_ping:
            return response(200, 'Ping payload validated', [])

        branch = payload['ref'].split('/')[-1]

        allowed_branches = set(validation_data.get('branches', branch))

        if branch not in allowed_branches:
            return response(
                403, 'Payload validation failed: wrong branch: %s' %
                branch, [])

        return response(200, 'Payload validated. Branch: %s' %
                        branch, [{'branch': branch}])

    except Exception as e:
        return response(400, 'Payload validation failed: %s' % e, [])
