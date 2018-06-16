from apps.common import seed
from trezor.messages.TezosPublicKey import TezosPublicKey
from trezor.crypto.curve import ed25519
from apps.wallet.get_public_key import _show_pubkey

from apps.tezos.helpers import TEZOS_CURVE


async def tezos_get_public_key(ctx, msg):
    address_n = msg.address_n or ()
    node = await seed.derive_node(ctx, address_n, TEZOS_CURVE)
            
    sk = node.private_key()
    pk = ed25519.publickey(sk)

    if msg.show_display:
        await _show_pubkey(ctx, pk)

    return TezosPublicKey(public_key=pk)
