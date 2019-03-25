from ubinascii import hexlify

from trezor import wire
from trezor.crypto.curve import secp256k1
from trezor.crypto.hashlib import sha256
from trezor.utils import HashWriter
from trezor.messages.OnegramSignedTx import OnegramSignedTx

from apps.common.writers import write_bytes
from apps.onegram import layout
from apps.onegram import writers


async def sign_tx(ctx, msg, keychain):
    check(msg)
    node = keychain.derive(msg.address_n, "secp256k1")

    await layout.require_confirm_tx(ctx, msg.source, msg.destination,
                                    msg.amount.amount)
    await layout.require_confirm_fee(ctx, msg.amount.amount, msg.fee.amount)

    w = bytearray()
    ch_id = bytearray()

    write_bytes(ch_id, msg.chain_id)
    writers.write_common(w, msg)
    writers.write_transfer(w, msg)

    sign_digest = HashWriter(sha256(ch_id + w)).get_digest()

    signature = secp256k1.sign(
            node.private_key(), sign_digest, True, secp256k1.CANONICAL_SIG_ONEGRAM
    )

    tx_digest = HashWriter(sha256(w)).get_digest()
    tx_hash = hexlify(tx_digest[:20]).decode('ascii')

    return OnegramSignedTx(signature=signature, tx_hash=tx_hash)


def check(msg: OnegramSignTx):
    if msg.chain_id is None:
        raise wire.DataError("No chain id provided")
    if msg.header is None:
        raise wire.DataError("No header provided")
