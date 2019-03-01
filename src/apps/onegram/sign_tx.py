from trezor.crypto.hashlib import sha256
from trezor.utils import HashWriter

from apps.onegram import updaters


async def sign_tx(ctx, msg, keychain):
    check(msg)

    node = await keychain.derive(msg.address_n, "secp256k1")

    sha = HashWriter(sha256)
    updaters.update_common(sha, msg)
    updaters.update_transfer(sha, msg)

    digest = sha.get_digest()
    signature = secp256k1.sign(
            node.private_key(), digest, True, secp256k1.CANONICAL_SIG_EOS  # TODO: OGC CANONICAL
    )

    return OnegramSignedTx(signature=signature) # TODO: tx hash


def check(msg: OnegramSignTx):
    if msg.chain_id is None:
        raise wire.DataError("No chain id provided")
    if msg.header is None:
        raise wire.DataError("No header provided")
