from trezor.crypto.curve import nist256p1
from trezor.crypto.hashlib import sha256

from apps.common import seed


async def sign(ctx, address_n, raw_data: bytes) -> bytes:
    """
    Creates signature for data
    """
    data_hash = sha256(sha256(sha256(raw_data).digest()).digest()).digest()

    node = await seed.derive_node(ctx, address_n, "nist256p1")

    signature = nist256p1.sign(node.private_key(), data_hash, False)
    signature = b"\x01" + signature[1:65]  # first byte of transaction is 0x01
    return signature
