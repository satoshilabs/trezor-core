from trezor.crypto.curve import secp256k1
from trezor.messages.TronAddress import TronAddress

from .helpers import get_address_from_public_key

from apps.common import seed
from apps.common.layout import show_address, show_qr


async def get_address(ctx, msg):
    address_n = msg.address_n or ()
    node = await seed.derive_node(ctx, address_n)
    seckey = node.private_key()
    public_key = secp256k1.publickey(seckey, False)
    address = get_address_from_public_key(public_key[:65])

    if msg.show_display:
        while True:
            if await show_address(ctx, address):
                break
            if await show_qr(ctx, address):
                break

    return TronAddress(address=address)
