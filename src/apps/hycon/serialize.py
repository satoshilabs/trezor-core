from trezor.messages.HyconSignTx import HyconSignTx
from apps.common.writers import write_bytes
from . import helpers

# PROTOBUF3 types
TYPE_VARINT = 0
TYPE_64BIT = 1
TYPE_STRING = 2
TYPE_GROUPS = 3
TYPE_GROUPE = 4
TYPE_FLOAT = 5


def add_field(w, fnumber, ftype):
    if fnumber > 15:
        w.append(fnumber << 3 | ftype)
        w.append(0x01)
    else:
        w.append(fnumber << 3 | ftype)


def write_varint(w, value):
    """
    Implements Base 128 variant
    See: https://developers.google.com/protocol-buffers/docs/encoding#varints
    """
    while True:
        byte = value & 0x7F
        value = value >> 7
        if value == 0:
            w.append(byte)
            break
        else:
            w.append(byte | 0x80)


def write_bytes_with_length(w, buf: bytearray):
    write_varint(w, len(buf))
    write_bytes(w, buf)

def serialize(tx: HyconSignTx, address: str):
    # transaction parameters
    ret = bytearray()
    
    add_field(ret, 1, TYPE_STRING)
    write_bytes_with_length(ret, helpers.address_to_byte_array(address))
    add_field(ret, 2, TYPE_STRING)
    write_bytes_with_length(ret, helpers.address_to_byte_array(tx.to))
    add_field(ret, 3, TYPE_VARINT)
    write_varint(ret, helpers.hycon_from_string(tx.amount))
    add_field(ret, 4, TYPE_VARINT)
    write_varint(ret, helpers.hycon_from_string(tx.fee))
    add_field(ret, 5, TYPE_VARINT)
    write_varint(ret, tx.nonce)
    add_field(ret, 10, TYPE_STRING)
    write_bytes_with_length(ret, "hycon")

    return ret