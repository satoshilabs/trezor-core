from trezor.crypto import base58


PREFIXES = {
    'tz1': [6, 161, 159],
    'edpk': [13, 15, 37, 217],
    'edsk': [43, 246, 78, 7],
    'edsig': [9, 245, 205, 134, 18],
    'o': [5, 116],
    'KT1': [2, 90, 121]
}

TEZOS_CURVE = 'ed25519'


def b58cencode(payload, prefix=None):
    payload = list(payload)
    result = payload
    if prefix is not None:
        result = PREFIXES[prefix] + payload
    return base58.encode_check(bytes(result))


def b58cdecode(enc, prefix=None):
    decoded = base58.decode_check(enc)
    if prefix is not None:
        decoded = decoded[len(PREFIXES[prefix]):]
    return decoded
