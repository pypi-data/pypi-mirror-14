""" Reads claviger's configuration file. """
import yaml
import logging
import os.path
import textwrap
import itertools
import collections

import six
import tarjan
import jsonschema

import claviger.authorized_keys

class ConfigError(Exception):
    pass

ParsedServerKey = collections.namedtuple('ParsedServerKey',
                                    ('hostname', 'user', 'port', 'abstract'))

l = logging.getLogger(__name__)

# Schema for the configuration file.
_SCHEMA = None

def get_schema():
    global _SCHEMA
    if not _SCHEMA:
        l.debug('loading scheme ...')
        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                'config.schema.yml')) as f:
            _SCHEMA = yaml.load(f)
        l.debug('    ... done!')
    return _SCHEMA

class ConfigurationError(Exception):
    pass

def parse_server_key(key):
    """ Converts a server key like (root@host:1234 or just host)
                to a triplet (user, port, hostname, abstract) """
    port = None
    user = None
    abstract = False
    hostname = None
    if key.startswith('$'):
        abstract = True
    else:
        hostname = key
        if ':' in hostname:
            hostname, _port = hostname.rsplit(':', 1)
            port = int(_port)
        if '@' in hostname:
            user, hostname = hostname.split('@', 1)
    return ParsedServerKey(user=user, port=port, hostname=hostname,
                                abstract=abstract)

def load(path):
    """ Loads the configuration file.
    
        A lot of the work is done by YAML.  We validate the easy bits with
        a JSON schema. The rest by hand. """
    # TODO Cache schema and configuration file
    l.debug('loading configuration file ...')
    with open(path) as f:
        cfg = yaml.load(f)

    l.debug('  - checking schema')
    # First small fixes which the schema can't handle
    cfg.setdefault('servers', {})
    cfg['servers'].setdefault('$default', {})
    for key in cfg['servers']:
        if cfg['servers'][key] is None:
            cfg['servers'][key] = dict()

    # Now check the schema
    jsonschema.validate(cfg, get_schema())
    # TODO format into pretty error message

    l.debug('  - processing keys')
    new_keys = {}
    cfg.setdefault('keys', {})
    for key_name, key in six.iteritems(cfg['keys']):
        # TODO handle error
        entry = claviger.authorized_keys.Entry.parse(key)
        new_key = {'key': entry.key,
                   'options': entry.options,
                   'comment': entry.comment,
                   'keytype': entry.keytype}
        new_keys[key_name] = new_key
    cfg['keys'] = new_keys

    l.debug('  - processing server stanza short-hands')
    new_servers = {}
    for server_key, server in six.iteritems(cfg['servers']):
        parsed_server_key = parse_server_key(server_key)
        server.setdefault('name', server_key)
        server_name = server['name']
        server.setdefault('port', parsed_server_key.port)
        server.setdefault('user', parsed_server_key.user)
        server.setdefault('hostname', parsed_server_key.hostname)
        server.setdefault('ssh_user', server['user'])
        server.setdefault('present', [])
        server.setdefault('absent', [])
        server.setdefault('allow', [])
        server.setdefault('keepOtherKeys')
        server.setdefault('like', '$default' if server_key != '$default'
                                        else None)
        server.setdefault('abstract', parsed_server_key.abstract)
        prabsent = frozenset(server['present']) & frozenset(server['absent'])
        if prabsent:
            raise ConfigurationError(
                "Keys {0} are required to be both present and absent on {1}"
                    .format(tuple(prabsent), server_name))
        ablow = frozenset(server['allow']) & frozenset(server['absent'])
        if ablow:
            raise ConfigurationError(
                "Keys {0} are listed allowed and absent on {1}"
                    .format(tuple(ablow), server_name))
        for key_name in itertools.chain(server['present'], server['absent'],
                                        server['allow']):
            if not key_name in cfg['keys']:
                "Key {0} (on {1}) does not exist".format(key_name, server_name)
        if server_name in new_servers:
            raise ConfigurationError(
                "Duplicate server name {0}".format(server_name))
        new_servers[server_name] = server
    cfg['servers'] = new_servers

    l.debug('  - resolving server stanza inheritance')
    # create dependancy graph and use Tarjan's algorithm to find a possible
    # order to evaluate the server stanzas.
    server_dg = {server_name: [server['like']] if server['like'] else []
                    for server_name, server in six.iteritems(cfg['servers'])}
    for server_cycle_names in tarjan.tarjan(server_dg):
        if len(server_cycle_names) != 1:
            raise ConfigurationError(
                    "There is a cyclic dependacy among the servers {0}".format(
                                server_cycle_names))
        target_server = cfg['servers'][server_cycle_names[0]]
        if not target_server['like']:
            continue
        if not target_server['like'] in cfg['servers']:
            pass
        source_server = cfg['servers'][target_server['like']]

        # First the simple attributes
        for attr in ('port', 'user', 'hostname', 'ssh_user',
                        'keepOtherKeys'):
            if attr in source_server:
                if target_server[attr] is None:
                    target_server[attr] = source_server[attr]

        # Now, the present/absent/allow lists
        for key in source_server['present']:
            if key in target_server['absent']:
                continue
            if key not in target_server['present']:
                target_server['present'].append(key)
        for key in source_server['absent']:
            if (key in target_server['present']
                    or key in target_server['allow']):
                continue
            if key not in target_server['absent']:
                target_server['absent'].append(key)
        for key in source_server['allow']:
            if key in target_server['absent']:
                continue
            if key not in target_server['allow']:
                target_server['allow'].append(key)

    l.debug('  - setting defaults on server stanzas')
    for server in six.itervalues(cfg['servers']):
        for attr, dflt in (('port', 22),
                           ('user', 'root'),
                           ('keepOtherKeys', True)):
            if server[attr] is None:
                server[attr] = dflt
        
    l.debug('         ... done')

    return cfg
