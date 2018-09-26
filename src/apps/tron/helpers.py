from trezor.crypto import base58
from trezor.crypto.hashlib import sha3_256


def get_address_from_public_key(pubkey):
    address = b"\x41" + sha3_256(pubkey[1:65], keccak=True).digest()[12:32]
    return _address_base58(address)


def _address_base58(address):
    return base58.encode_check(address)


def _b58b(address):
    return base58.encode_check(bytes(address))
