from apps.common import seed
from apps.wallet.get_address import _show_address, _show_qr
from trezor.crypto import hashlib
from trezor.messages.TezosAddress import TezosAddress
from trezor.crypto.curve import ed25519

from apps.tezos.helpers import b58cencode, TEZOS_CURVE


async def tezos_get_address(ctx, msg):
    address_n = msg.address_n or ()
    node = await seed.derive_node(ctx, address_n, TEZOS_CURVE)

    sk = node.private_key()
    pk = ed25519.publickey(sk)
    pkh = hashlib.blake2b(pk, 20).digest()
    address = b58cencode(pkh, prefix='tz1')

    if msg.show_display:
        while True:
            if await _show_address(ctx, address):
                break
            if await _show_qr(ctx, address):
                break

    return TezosAddress(address=address)
