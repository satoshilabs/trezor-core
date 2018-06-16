from apps.common import seed
from trezor.messages.TezosSignedTx import TezosSignedTx
from trezor.crypto import hashlib
from trezor.crypto.curve import ed25519

from apps.tezos.helpers import b58cencode, TEZOS_CURVE
from apps.tezos.layout import *


async def tezos_sign_tx(ctx, msg):
    address_n = msg.address_n or ()
    node = await seed.derive_node(ctx, address_n, TEZOS_CURVE)

    operation_bytes = msg.operation_bytes
    operation_hashed_bytes = hashlib.blake2b(operation_bytes, 32).digest()
    signature = ed25519.sign(node.private_key(), operation_hashed_bytes)

    sig_op_contents = operation_bytes + signature
    sig_op_contents_blaked = hashlib.blake2b(sig_op_contents, 32).digest()
    operation_hash = b58cencode(sig_op_contents_blaked, prefix='o')

    await require_confirm_tx(ctx, msg.to, msg.value)
    await require_confirm_fee(ctx, msg.value, msg.fee)

    return TezosSignedTx(signature=signature,
                         sig_op_contents=sig_op_contents,
                         operation_hash=operation_hash)
