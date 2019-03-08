from ubinascii import hexlify

from trezor import wire
from trezor.crypto.curve import secp256k1
from trezor.crypto.hashlib import sha256
from trezor.utils import HashWriter
from trezor.messages.OnegramSignedTx import OnegramSignedTx

from apps.onegram import layout
from apps.onegram import writers


async def sign_tx(ctx, msg, keychain):
    check(msg)
    node = keychain.derive(msg.address_n, "secp256k1")

    await layout.require_confirm_tx(ctx, msg.source, msg.destination,
                                    msg.amount.amount)
    await layout.require_confirm_fee(ctx, msg.amount.amount, msg.fee.amount)

    w = bytearray()
    writers.write_common(w, msg)
    writers.write_transfer(w, msg)

    hasher = HashWriter(sha256(w))
    digest = hasher.get_digest()

    signature = secp256k1.sign(
            node.private_key(), digest, True, secp256k1.CANONICAL_SIG_ONEGRAM
    )

    tx_hash = hexlify(digest[:20]).decode('ascii')
    return OnegramSignedTx(signature=signature, tx_hash=tx_hash)


def check(msg: OnegramSignTx):
    if msg.chain_id is None:
        raise wire.DataError("No chain id provided")
    if msg.header is None:
        raise wire.DataError("No header provided")
