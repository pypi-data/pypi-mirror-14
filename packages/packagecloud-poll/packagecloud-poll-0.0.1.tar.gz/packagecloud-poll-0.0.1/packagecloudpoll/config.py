import os

from schema import Schema, Use, And, SchemaError

import utils


def load_env():
    """
    Reads environment looking for token and returns config.
    """
    token = os.environ.get('PACKAGECLOUD_TOKEN')
    if token is None:
        utils.abort('PACKAGECLOUD_TOKEN environment variable is not set. '
                    'Set this token to use packagecloud-poll.')
    http_scheme = 'https'
    api_domain = 'packagecloud.io'
    api_version = 'v1'
    return {
        'url_base': '{}://{}:@{}/api/{}'.format(
            http_scheme, token, api_domain, api_version),
        'token': token
    }


def validate_args(args):
    """
    Validates command line arguments
    """
    schema = Schema({
        '--user': And(str, len, Use(str.lower), error="missing or invalid user"),
        '--repo': And(str, len, Use(str.lower), error="missing or invalid repo"),
        '--type': And(str, len, Use(str.lower), lambda s: s in ('deb', 'rpm'), error="type must be one of deb or rpm"),
        '--distro': And(str, len, Use(str.lower), error="missing or invalid distro"),
        '--distro_version': And(str, len, Use(str.lower), error="missing or invalid distro_version"),
        '--arch': And(str, len, Use(str.lower), error="missing or invalid arch"),
        '--pkg_name': And(str, len, Use(str.lower), error="missing or invalid pkg_name"),
        '--filename': And(str, len, Use(str.lower), error="missing or invalid filename"),
        '--timeout': And(Use(float), lambda f: f > 0, lambda f, i=float(args['--poll_interval']): f > i,
                         error="timeout must be a number greater than 1, and greater than poll_interval (default 30)"),
        '--poll_interval': And(Use(float), lambda f: f > 0, error="poll_interval must be a number greater than 0"),
        '--help': bool,
        '--version': bool,
        '--log-level': And(str, len, Use(str.upper),
                           lambda s: s in ('DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL'),
                           error="invalid log level specified")
    })

    try:
        return schema.validate(args)
    except SchemaError as ex:
        utils.abort("Invalid argument: {}. ".format(ex.message))
