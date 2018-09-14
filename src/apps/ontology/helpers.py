from trezor.crypto import base58
from trezor.crypto.hashlib import ripemd160, sha256


def get_address_from_public_key(pubkey: bytes) -> str:
    """
    Computes address from public key
    """
    hex_address = (
        b"\x17" + ripemd160(sha256(b"\x21" + pubkey + b"\xac").digest()).digest()
    )
    return base58.encode_check(hex_address)


def get_hex_from_address(address: str) -> bytes:
    """
    Converts base58check address to hex representation
    """
    return base58.decode_check(address)[1:]
