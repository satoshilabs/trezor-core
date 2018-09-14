from trezor.crypto.curve import nist256p1
from trezor.messages.OntologyAddress import OntologyAddress

from .helpers import get_address_from_public_key

from apps.common import seed
from apps.common.layout import show_address, show_qr


async def get_address(ctx, msg):
    address_n = msg.address_n or ()
    node = await seed.derive_node(ctx, address_n, "nist256p1")

    seckey = node.private_key()
    public_key = nist256p1.publickey(seckey, True)
    address = get_address_from_public_key(public_key)

    if msg.show_display:
        while True:
            if await show_address(ctx, address):
                break
            if await show_qr(ctx, address):
                break

    return OntologyAddress(address=address)
