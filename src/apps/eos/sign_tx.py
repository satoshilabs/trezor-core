from trezor import wire
from trezor.crypto.curve import secp256k1
from trezor.crypto.hashlib import sha256
from trezor.messages.EosSignedTx import EosSignedTx
from trezor.messages.EosSignTx import EosSignTx
from trezor.messages.EosTxActionRequest import EosTxActionRequest
from trezor.utils import HashWriter

from apps.common import seed
from apps.eos import consts, updaters
from apps.eos.actions import process_action
from apps.eos.layout import require_sign_tx


async def sign_tx(ctx, msg: EosSignTx):
    check(msg)

    node = await seed.derive_node(ctx, msg.address_n)
    sha = HashWriter(sha256)
    await _init(ctx, sha, msg)
    await _actions(ctx, sha, msg.num_actions)
    updaters.hashupdate_variant32(sha, 0)
    updaters.hashupdate_bytes(sha, bytearray(32))

    digest = sha.get_digest()
    signature = secp256k1.sign(
        node.private_key(), digest, True, secp256k1.CANONICAL_SIG_EOS
    )

    resp = EosSignedTx()
    resp.signature_v = signature[0]
    resp.signature_r = signature[1:33]
    resp.signature_s = signature[33:]

    return resp


async def _init(ctx, sha, msg):
    updaters.hashupdate_bytes(sha, msg.chain_id)
    updaters.hashupdate_header(sha, msg.header)
    updaters.hashupdate_variant32(sha, 0)
    updaters.hashupdate_variant32(sha, msg.num_actions)

    await require_sign_tx(ctx, msg.num_actions)


async def _actions(ctx, sha, num_actions: int):
    for i in range(num_actions):
        action = await ctx.call(EosTxActionRequest(), *consts.action_wire_types)
        await process_action(ctx, sha, action)


def check(msg: EosSignTx):
    if msg.chain_id is None:
        raise wire.DataError("No chain id")
    if msg.header is None:
        raise wire.DataError("No header")
    if msg.num_actions == 0:
        raise wire.DataError("No actions")
