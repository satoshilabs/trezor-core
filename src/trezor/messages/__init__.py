from trezor import log
from . import wire_types

# Reverse table of wire_types
type_to_name = {}

# Dynamically registered messages
registered = {}


def register(cls):
    '''Register custom message type in runtime.'''

    if __debug__:
        log.debug(__name__, 'Registering %s' % cls)

    registered[cls.MESSAGE_WIRE_TYPE] = cls


def get_type(wire_type):
    '''Get message class for handling given wire_type.'''

    # Lookup to dynamically built table
    if wire_type in registered:
        return registered[wire_type]

    name = type_to_name[wire_type]
    module = __import__('trezor.messages.%s' % name, None, None, (name, ), 0)
    return getattr(module, name)


def build_type_to_name():
    '''Build reverse table of wire_types.'''

    if __debug__:
        log.debug(__name__, 'Building wire_types reverse table')

    for name in dir(wire_types):
        type_to_name[getattr(wire_types, name)] = name


build_type_to_name()
