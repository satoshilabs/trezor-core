from trezor.crypto.curve import nist256p1
from trezor.messages.OntologyPublicKey import OntologyPublicKey

from apps.common import layout, seed


async def get_public_key(ctx, msg):
    address_n = msg.address_n or ()
    node = await seed.derive_node(ctx, address_n, "nist256p1")

    seckey = node.private_key()
    public_key = nist256p1.publickey(seckey, True)

    if msg.show_display:
        await layout.show_pubkey(ctx, public_key)

    return OntologyPublicKey(public_key=public_key)
