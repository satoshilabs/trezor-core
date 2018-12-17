from trezor.crypto import der
from trezor.crypto.curve import secp256k1
from trezor.messages.HyconSignedTx import HyconSignedTx
from trezor.messages.HyconSignTx import HyconSignTx
from trezor.wire import ProcessError

from . import helpers, layout

from apps.common import paths
from apps.hycon.serialize import serialize
from .base58_hycon import blake2b_hash

def sign(hash: bytes, private_key: bytes):
    sign = secp256k1.sign(private_key, hash)
    recovery = sign[0] - 31
    signature = sign[1:33] + sign[33:65]

    return signature, recovery

async def sign_tx(ctx, msg: HyconSignTx, keychain):
    validate(msg)
    await paths.validate_path(ctx, helpers.validate_full_path, path=msg.address_n)

    node = keychain.derive(msg.address_n)
    source_address = helpers.address_from_public_key(node.public_key())
    source_address_str = helpers.address_to_string(source_address)

    check_fee(msg.fee)
    await layout.require_confirm_fee(ctx, msg.fee)
    await layout.require_confirm_tx(ctx, source_address_str, msg.amount)

    proto_tx = serialize(msg, source_address_str)
    txhash = blake2b_hash(proto_tx)

    result = sign(txhash, node.private_key())

    return HyconSignedTx(helpers.bytes_to_hex_string(result[0]), result[1], helpers.bytes_to_hex_string(txhash))


def check_fee(fee: str):
    if helpers.hycon_from_string(fee) < helpers.MIN_FEE:
        raise ProcessError("Fee must be more than 0.000000001")


def validate(msg: HyconSignTx):
    if None in (msg.fee, msg.nonce, msg.amount, msg.to):
        raise ProcessError(
            "Some of the required fields are missing (fee, nonce, amount, to address)"
        )
