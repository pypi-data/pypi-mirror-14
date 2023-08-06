import os
import copy

from bigchaindb.core import Bigchain  # noqa


def e(key, default=None, conv=None):
    '''Get the environment variable `key`, fallback to `default`
    if nothing is found.

    Keyword arguments:
    key -- the key to look for in the environment
    default -- the default value if nothing is found (default: None)
    conv -- a callable used to convert the value (default: use the type of the
            default value)
    '''

    val = os.environ.get(key, default)

    if conv or default is not None:
        conv = conv or type(default)
        return conv(val)

    return val


config = {
    'database': {
        'host': e('BIGCHAIN_DATABASE_HOST', default='localhost'),
        'port': e('BIGCHAIN_DATABASE_PORT', default=28015),
        'name': e('BIGCHAIN_DATABASE_NAME', default='bigchain')
    },
    'keypair': {
        'public': e('BIGCHAIN_KEYPAIR_PUBLIC'),
        'private': e('BIGCHAIN_KEYPAIR_PRIVATE')
    },
    'keyring': [
    ]
}

# We need to maintain a backup copy of the original config dict in case
# the user wants to reconfigure the node. Check ``bigchaindb.config_utils``
# for more info.
_config = copy.deepcopy(config)
