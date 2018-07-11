from trezor import wire
from trezor.crypto import base58
from trezor.crypto.curve import ed25519, nist256p1, secp256k1

PREFIXES = {
    # addresses
    "tz1": [6, 161, 159],
    "tz2": [6, 161, 161],
    "tz3": [6, 161, 164],
    "KT1": [2, 90, 121],
    # public keys
    "edpk": [13, 15, 37, 217],
    "sppk": [3, 254, 226, 86],
    "p2pk": [3, 178, 139, 127],
    # operation hash
    "o": [5, 116],
}

TEZOS_CURVES = [
    {
        "name": "ed25519",
        "address_prefix": "tz1",
        "pk_prefix": "edpk",
        "module": ed25519,
    },
    {
        "name": "secp256k1",
        "address_prefix": "tz2",
        "pk_prefix": "sppk",
        "module": secp256k1,
    },
    {
        "name": "nist256p1",
        "address_prefix": "tz3",
        "pk_prefix": "p2pk",
        "module": nist256p1,
    },
]


def get_curve_name(index):
    if 0 <= index < len(TEZOS_CURVES):
        return TEZOS_CURVES[index]["name"]
    raise wire.DataError("Invalid type of curve")


def get_curve_module(curve):
    return TEZOS_CURVES[curve]["module"]


def get_address_prefix(curve):
    return TEZOS_CURVES[curve]["address_prefix"]


def get_pk_prefix(curve):
    return TEZOS_CURVES[curve]["pk_prefix"]


def b58cencode(payload, prefix=None):
    payload = list(payload)
    result = payload
    if prefix is not None:
        result = PREFIXES[prefix] + payload
    return base58.encode_check(bytes(result))


def b58cdecode(enc, prefix=None):
    decoded = base58.decode_check(enc)
    if prefix is not None:
        decoded = decoded[len(PREFIXES[prefix]) :]
    return decoded
